# -*- coding: utf-8 -*-
# @Time    : 2019/5/4 9:09
# @Author  : Weiyang
# @File    : MatchCypher.py
'''
用于匹配Cypher语句和其相应槽位标记的类

输入：分类器的问题类别或规则匹配的问题类别，
输出：Cypher语句，槽位标记列表，以及查询值标记 例如 Cypher语句,[nnt,ng,x,nm],m.title
'''
from MyExceptionError import *
import traceback

class MatchCypher(object):
    '用于匹配Cypher语句和其相应槽位标记的类'

    def __init__(self,cfg):
        self.cfg = cfg # cfg是configparser.ConfigParser().read()对象
        # Cypher语句
        self.classifier_cypher = self.__getClassifierCypher() # 存储分类器处理的问题所对应的Cypher语句，数据结构：{label:cypher}
        self.rule_cypher = self.__getRuleCypher() # 存储规则处理的问题所对应Cypher语句,数据结构{label:cypher,...}
        # Cypher语句对应的槽位标记
        self.classifier_cypher_slot = self.__getClassifierCypherSlot() # 存储分类器对应的cypher语句的槽位标记列表,数据结构:{label:[slot1,slot2,..],..}
        self.rule_cypher_slot = self.__getRuleCypherSlot() # 存储规则对应的cypher语句的槽位标记列表,数据结构:{label:[slot1,slot2,..],..}
        # Cypher语句返回的值标记，用于从Cypher返回对象中获取确切的查询值,由py2neo cursor决定
        self.classifier_cypher_value = self.__getClassifierCypherSearchValue() # 存储分类器对应的cypher语句的查询值标记,数据结构:{label:value,..}
        self.rule_cypher_value = self.__getRuleCypherSearchValue() # 存储规则对应的cypher语句的查询值标记,数据结构:{label:value,..}

    def __defaultdict(self):
        '构建默认词典'
        from collections import defaultdict
        mydict = defaultdict(str)
        return mydict

    def __getClassifierCypher(self):
        '构建 分类器处理的问题类别与cypher语句的映射字典'
        mydict = self.__defaultdict()
        # 读取cypher语句
        for label,path in enumerate(self.cfg.options('classifierTemplate')):
            mydict[label] = self.cfg.get('classifierTemplate',path) # 获取cypher
        return mydict

    def __getRuleCypher(self):
        '构建 规则处理的问题类别与cypher语句的映射字典'
        mydict = self.__defaultdict()
        # 读取cypher语句
        for label, path in enumerate(self.cfg.options('ruleTemplate')):
            mydict[label] = self.cfg.get('ruleTemplate', path)  # 获取cypher
        return mydict

    def __getClassifierCypherSlot(self):
        '构建 分类器处理的问题类别与cypher语句槽位标记列表的映射字典'
        mydict = self.__defaultdict()
        for label,slot in enumerate(self.cfg.options('classifierTemplateSlot')):
            slots = self.cfg.get('classifierTemplateSlot',slot) # 槽位标记可能是多个，需要切割
            mydict[label] = slots.strip().split()
        return mydict

    def __getRuleCypherSlot(self):
        '构建 分类器处理的问题类别与cypher语句槽位标记列表的映射字典'
        mydict = self.__defaultdict()
        for label,slot in enumerate(self.cfg.options('ruleTemplateSlot')):
            slots = self.cfg.get('ruleTemplateSlot',slot) # 槽位标记可能是多个，需要切割
            mydict[label] = slots.strip().split()
        return mydict

    def __getClassifierCypherSearchValue(self):
        '构建 分类器处理的问题类别与cypher语句槽位标记列表的映射字典'
        mydict = self.__defaultdict()
        for label,value in enumerate(self.cfg.options('classifierTemplateSearchValue')):
            mydict[label] = self.cfg.get('classifierTemplateSearchValue',value).strip()
        return mydict

    def __getRuleCypherSearchValue(self):
        '构建 分类器处理的问题类别与cypher语句槽位标记列表的映射字典'
        mydict = self.__defaultdict()
        for label,value in enumerate(self.cfg.options('ruleTemplateSearchValue')):
            mydict[label] = self.cfg.get('ruleTemplateSearchValue',value).strip()
        return mydict

    def getCypher(self,label,flag=True):
        '根据类别获取cypher'
        'label是问题的类别，flag为True表示查询的是分类器处理的问题类别；为False，表示查询的是规则处理的问题类别'
        label = int(label) # 先将类别的数据类型转为一致，注意int与numpy.int32是不同的
        if flag:
            # 如果出现的类别不在我们预定义的类别中，则抛出异常
            try:
                if label not in self.classifier_cypher:
                    raise MyExceptionError('该类别编码不在我们预定义的分类器处理的问题类别中，请查看配置文件！')
            except MyExceptionError as e:
                print(e)
                print(traceback.format_exc()) # 打印堆栈信息
            cypher = self.classifier_cypher[label]
            slot = self.classifier_cypher_slot[label]
            value = self.classifier_cypher_value[label]
        else:
            # 如果出现的类别不在我们预定义的类别中，则抛出异常
            try:
                if label not in self.rule_cypher:
                    raise MyExceptionError('该类别编码不在我们预定义的规则处理的问题类别中，请查看配置文件！')
            except MyExceptionError as e:
                print(e)
                print(traceback.format_exc())  # 打印堆栈信息
            cypher = self.rule_cypher[label]
            slot = self.rule_cypher_slot[label]
            value = self.rule_cypher_value[label]

        return cypher,slot,value

if __name__ == '__main__':
    import configparser
    cfg = configparser.ConfigParser()
    cfg.read('../config/config.ini', encoding='utf-8')

    match = MatchCypher(cfg)

    print(match.classifier_cypher)
    print(match.classifier_cypher_slot)
    print(match.classifier_cypher_value)
    print('-'*30)
    print(match.rule_cypher)
    print(match.rule_cypher_slot)
    print(match.rule_cypher_slot)
    print('='*30)

    result = match.getCypher(label=5,flag=True)
    print(result)

    result = match.getCypher(label=3,flag=False)
    print(result)

    '''
    defaultdict(<class 'str'>, {0: 'match(m:Movie) where m.title="%s" return m.rating', 1: 'match(m:Movie) where m.title="%s" return m.releasedate', 2: 'match(m:Movie)-[r:is]->(g:Genre) where m.title="%s"  return g.name', 3: 'match(m:Movie) where m.title="%s" return m.introduction', 4: 'match(p:Actor)-[r:参演]->(m:Movie) where m.title="%s" return distinct p.name', 5: 'match(p:Actor) where p.name="%s" return p.biography', 6: 'match(p:Actor{name:"%s"})-[r:参演]->(m:Movie) with m match(m:Movie)-[r:is]->(g:Genre{name:"%s"}) return m.title', 7: 'match(p:Actor)-[r:参演]->(m:Movie) where p.name="%s" return m.title', 8: 'match(p:Actor)-[r:参演]->(m:Movie) where p.name="%s" and m.rating >= %.1f return m.title', 9: 'match(p:Actor)-[r:参演]->(m:Movie) where p.name="%s" and m.rating < %.1f return m.title', 10: 'match(p:Actor)-[r:参演]->(m:Movie) where p.name="%s" with m match(m:Movie)-[r:is]->(g:Genre) return distinct g.name', 11: 'match(p1:Actor)--(m:Movie)--(p2:Actor) where p1.name="%s" and p2.name="%s" return m.title', 12: 'match(p:Actor)-[r:参演]-(m:Movie) where p.name="%s" return count(m.title)', 13: 'match(p:Actor) where p.name="%s" return p.birth'})
    defaultdict(<class 'str'>, {0: ['nm'], 1: ['nm'], 2: ['nm'], 3: ['nm'], 4: ['nm'], 5: ['nnt'], 6: ['nnt', 'ng'], 7: ['nnt'], 8: ['nnt', 'x'], 9: ['nnt', 'x'], 10: ['nnt'], 11: ['nnt', 'nnt'], 12: ['nnt'], 13: ['nnt']})
    defaultdict(<class 'str'>, {0: 'm.rating', 1: 'm.releasedate', 2: 'g.name', 3: 'm.introduction', 4: 'p.name', 5: 'p.biography', 6: 'm.title', 7: 'm.title', 8: 'm.title', 9: 'm.title', 10: 'g.name', 11: 'm.title', 12: 'count(m.title)', 13: 'p.birth'})
    ------------------------------
    defaultdict(<class 'str'>, {0: 'match(m:Movie)-[r:is]->(g:Genre) where g.name="%s" return m.title', 1: 'match(m:Movie)-[r:is]->(g:Genre) where g.name="%s" and m.rating >= %.1f return m.title', 2: 'match(p:Actor)-[r1:参演]->(m:Movie)-[r2:is]->(g:Genre) where g.name="%s" return distinct p.name', 3: 'match(m:Movie) where m.rating >= %.1f return distinct m.title', 4: 'match(m:Movie)-[r:is]->(g:Genre) where g.name = "%s" and m.rating >= %.1f return distinct m.title', 5: 'match(p:Actor) where p.name="%s" return p.birthplace', 6: 'match(p:Actor)-[r:参演]->(m:Movie) where p.name="%s" and m.title="%s" return r.pid'})
    defaultdict(<class 'str'>, {0: ['ng'], 1: ['ng', 'x'], 2: ['ng'], 3: ['x'], 4: ['ng', 'x'], 5: ['nnt'], 6: ['nnt', 'nm']})
    defaultdict(<class 'str'>, {0: ['ng'], 1: ['ng', 'x'], 2: ['ng'], 3: ['x'], 4: ['ng', 'x'], 5: ['nnt'], 6: ['nnt', 'nm']})
    ==============================
    ('match(p:Actor) where p.name="%s" return p.biography', ['nnt'], 'p.biography')
    ('match(m:Movie) where m.rating >= %.1f return distinct m.title', ['x'], 'm.title')
    '''

    # 检查我们定义的异常是否正常运行
    #match.getCypher(label=20,flag=True)
