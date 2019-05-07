# -*- coding: utf-8 -*-
# @Time    : 2019/5/3 21:07
# @Author  : Weiyang
# @File    : RuleMatch.py

'''
用于规则匹配的类
程序输入：经过槽位标记处理后的文本数据,不是单词列表
程序输出：匹配到的规则类别列表，例如: [rule_1,rule_2,..]
规则类别用于映射Cypher语句
'''

class RuleMatch(object):

    def __init__(self,cfg):
        self.cfg = cfg # cfg是configparser.ConfigParser().read()对象
        self.rule2label = self.__getRule() # 存储规则到类别的映射表，数据结构是{'rule':label}

    def __rule2label(self):
        '构建默认词典'
        from collections import defaultdict
        mydict = defaultdict(str)
        return mydict

    def __getRule(self):
        '加载规则'
        rule2label = self.__rule2label()
        options = self.cfg.options('rule')
        # 循环加载规则数据
        for label,rule_path in enumerate(options):
            with open(self.cfg.get('rule',rule_path),'r',encoding='utf-8-sig') as fi:
                for line in fi:
                    rule2label[line.strip()] = label
        return rule2label

    def matchRule(self,text):
        '匹配规则，并返回规则的类别列表'
        'text是待匹配的文本数据'
        import re
        label = [] # 存储匹配到的规则类别
        # 遍历规则
        for rule in self.rule2label.keys():
            regx = re.compile(rule)
            result = regx.findall(text)
            # 如果匹配成功，则将规则对应的类别加入到类别列表中
            if result:
                label.append(self.rule2label[rule])
        # 对类别列表去重
        label = list(set(label))
        return label

if __name__ == '__main__':
    import configparser
    cfg = configparser.ConfigParser()
    cfg.read('../config/config.ini', encoding='utf-8')
    model = RuleMatch(cfg)
    print(model.rule2label)
    text = 'nnt参演了nm了吗'
    result = model.matchRule(text)
    print(result)

    '''
    defaultdict(<class 'str'>, {'ng.*[电影|影片|片子]': 0, '[电影|影片|片子].*ng': 0, 'ng.*[电影|影片|片子].*[得分|评分|打分].*[大于|大|高|高于|超过].*x': 1, '[出演|主演|演过|拍过].*ng.*nnt': 2, '[得分|评分|打分|分数].*[大于|大|高于|高|超过].*x': 3, '[得分|评分|打分|分数].*[大于|大|高于|高|超过].*x.*ng': 4, 'nnt.*[出生地|长大|成长|籍贯|国籍|哪国|]': 5, 'nnt.*[参演|出演|演过|拍|拍过|主演].*nm': 6, '[知道|会|能干|能做].*[什么|啥]': 7})
    [6]
    '''