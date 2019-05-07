# -*- coding: utf-8 -*-
# @Time    : 2019/5/5 18:39
# @Author  : Weiyang
# @File    : main.py
'''
后台主程序入口
'''

import jieba as jb
import configparser
import logging
import logging.handlers
from src.AutomaticSpeak import AutomaticSpeak
from src.ClassifierModel import ClassifierModel
from src.ConnectNeo4jSearch import ConnectNeo4jSearch
from src.FormatReply import FormatReply
from src.MatchCypher import MatchCypher
from src.NamedEntityRecognition import NamedEntityRecognition
from src.RewriteCypher import RewriteCypher
from src.RuleMatch import RuleMatch


def main():
    #-----------------------1. 程序启动准备工作----------------------

    # 读取配置
    cfg = configparser.ConfigParser()
    cfg.read('../config/config.ini', encoding='utf-8')
    # 日志配置
    #logging.basicConfig(level=cfg.getint('logConfig','logRecord_level')) # 如果设置此，会将level及其以上的级别信息都输出到控制台
    logger = logging.getLogger('main')
    logger.setLevel(level=cfg.getint('logConfig','logger_level'))
    handler = logging.handlers.RotatingFileHandler(filename=cfg.get('logConfig','LOG_PATH'),
                                            maxBytes=cfg.getint('logConfig','maxBytes'),
                                            backupCount=cfg.getint('logConfig','backupCount'))
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(cfg.get('logConfig','formatter'))
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # 读取用于判定是否接受分类器结果的阈值
    threshold = cfg.getfloat('threshold','threshold')
    # 加载自定义词典
    jb.load_userdict(cfg.get('customDict','genreDictPath'))
    jb.load_userdict(cfg.get('customDict','movieDictPath'))
    jb.load_userdict(cfg.get('customDict','actorDictPath'))
    jb.load_userdict(cfg.get('customDict','scoreDictPath'))
    # 创建AutomaticSpeak实例
    autoSpeak = AutomaticSpeak()
    # 创建NamedEntityRecognition实例
    ner = NamedEntityRecognition(cfg)
    # 创建RuleMatch实例
    ruleMatch = RuleMatch(cfg)
    # 创建ClassifierModel实例
    classifierModel = ClassifierModel(cfg)
    # 创建MatchCypher实例
    matchCypher = MatchCypher(cfg)
    # 创建RewriteCypher实例
    rewriteCypher = RewriteCypher()
    # 创建ConnectNeo4jSearch实例
    connectNeo4jSearch = ConnectNeo4jSearch(cfg)
    # 创建FormatReply实例
    fr = FormatReply()

    #---------------------------2. 开始对话----------------------------

    # 首次启动，输出欢迎语
    speak = autoSpeak.firstSpeak()
    print('AI: ',speak)
    # 开启会话
    while True:
        # 获取用户输入
        text = input('我: ')
        # 判断用户输入是否是quit
        if text == 'quit':
            print('AI: ',autoSpeak.lastSpeak())
            break
        # 分词
        wordlst = list(jb.cut(text))
        # 命名实体识别
        # words:实体被槽位标记替换后的单词列表，slotDict:槽位标记对应的实体列表，count: 是槽位标记总数
        words,slotDict,count = ner.getSlot(wordlst)

        # 匹配规则
        rule_label = ruleMatch.matchRule(''.join(words))
        # 判断规则匹配是否成功,可能匹配到多条规则
        # 如果规则对应的槽位标记与输入中的槽位标记相同，或者该规则的槽位标记数量是匹配到的最多的
        # 则采纳规则，可以采纳多条规则；
        if rule_label != []:
            # 存储规则对应的Cypher语句,槽位标记列表，查询值标记
            results = []
            # 判断存储规则类别7是否存在的标记,规则类别7没有对应的cypher语句，需要单独处理
            flag = False
            # 遍历匹配到的规则编号，获取相应规则对应
            for labelID in rule_label:
                if labelID == 8:
                    flag = True
                    continue
                # 日志记录
                logger.info(':' + text + ':' + 'rule' + ':' + str(labelID))  # 将用户输入与分类器分类的结果输出，用于后期改进规则
                # result = (cypher,slotlst,searchValue)
                # cypher：查询语句,slotlst：槽位标记列表，searchValue: cypher语句返回的目标标记
                result = matchCypher.getCypher(label=labelID,flag=False)
                results.append(result)
            # 如果没有匹配到其它类别,且只识别到类别7
            if results == [] and flag:
                # 告知用户程序的能力
                print('AI: ',autoSpeak.rule8Speak())
                continue
            # 选择规则，也就是选择保留的cypher语句
            temp = [] # 存储results中的三元组
            # num用来记录先前cypher语句对应的槽位标记数量，如果大于这个值，则清空temp,并将当前值添加进去；
            # 如果等于这个值，则将当前值添加进去即可；如果小于这个值，则舍弃当前值
            num = 0
            for cypher,slotlst,searchValue in results:
                if num < len(slotlst):
                    num = len(slotlst)
                    temp = []
                    temp.append((cypher,slotlst,searchValue))
                elif num == len(slotlst):
                    temp.append((cypher, slotlst, searchValue))
                else:
                    pass
            results = temp  # 规则匹配到的cypher语句
        else:
            # 规则匹配不成功，则用分类器进行匹配
            # 先将输入文本转为词向量,此处的输入文本是分词后，并且槽位标记替换过的 词列表
            word2vec = classifierModel.getData(words)
            # 分类器分类
            labelID,proba = classifierModel.predict(word2vec)
            logger.info(':'+text+':'+'class'+':'+str(labelID)) # 将用户输入与分类器分类的结果输出，用于后期改进模型
            # 判定是否接受分类器结果
            if proba < threshold:
                # 请用户重新说明问题
                print('AI: ',autoSpeak.sorrySpeak())
                continue
            # 获取label对应的cypher语句，分类器只会识别出一个类别
            cypher,slotlst,searchValue = matchCypher.getCypher(label=labelID,flag=True)
            results = [(cypher,slotlst,searchValue)] # 格式要与上文的results一致，方便下面处理

        # 改写cypher语句，即将槽位的实际值填充进cypher语句
        searchResults = [] # 存储从知识图谱中查询到的结果,实际上每个值是一个可迭代的对象
        for cypher,slotlst,searchValue in results:
            # 槽位标记被实际值替换后，改写成功的cypher语句
            statement = rewriteCypher.run(cypher,slotlst,slotDict)
            # 判断改写是否成功
            if statement == None:
                continue
            # 查询知识图谱，获取结果
            result = connectNeo4jSearch.getSearchResult(statement=statement,value=searchValue)
            searchResults.append(result)
        # 格式化查询结果
        endResults = [] # 存储待输出的结果
        for result in searchResults:
            result = fr.formatReply(result)
            if result == '':
                continue
            endResults.append(str(result))
        # 判断查询结果中是否有实际内容
        if endResults == []:
            # 告知用户，程序没有收录问题的结果，请问其它问题
            logger.warning(':'+text) # 将知识图谱未收录的内容输出，用于改进知识图谱
            print('AI: ',autoSpeak.unknownSpeak())
            continue
        else:
            # 输出查询结果到用户界面
            # 由于查询获得的输出可能比较长，因此需要控制每行输出的内容，使得输出直观
            # 将输出转为一个长文本的字符串
            temp = list(','.join(endResults))
            # 我们每隔num个字符进行换行
            endResults = []
            num = 80
            for i in range(0,len(temp)):
                if i % num == 0 and i != 0:
                    endResults.append('\n')
                endResults.append(temp[i])
            print('AI: ',''.join(endResults))

if __name__ == '__main__':
    main()