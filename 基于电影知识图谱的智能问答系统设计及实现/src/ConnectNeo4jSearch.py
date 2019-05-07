# -*- coding: utf-8 -*-
# @Time    : 2019/5/4 10:55
# @Author  : Weiyang
# @File    : ConnectNeo4jSearch.py

'''
输入槽位填充上实际的值的Cypher语句，连接neo4j数据库进行查询，并返回结果
'''

class ConnectNeo4jSearch(object):
    '输入Cypher语句，连接neo4j数据库，查询，并返回结果'
    def __init__(self,cfg):
        self.cfg = cfg # cfg是configparser.ConfigParser().read()对象
        self.graph = self.__connectNeo4j() # neo4j的连接对象

    def __connectNeo4j(self):
        '连接数据库'
        from py2neo import Graph
        username = self.cfg.get('neo4j','username')
        password = self.cfg.get('neo4j','password')
        graph = Graph('http://localhost:7474',username=username,password=password)
        return graph

    def getSearchResult(self,statement,value):
        '输入Cypher语句，查询数据库，并返回结果'
        'statement是Cypher语句,value是查询的返回值标记，用于从cursor中抽取结果'
        cursor = self.graph.run(statement)
        # 用生成器，循环返回查询结果
        while cursor.forward():
            yield cursor.current[value]

if __name__ == '__main__':
    import configparser
    cfg = configparser.ConfigParser()
    cfg.read('../config/config.ini', encoding='utf-8')

    cns = ConnectNeo4jSearch(cfg)
    for result in cns.getSearchResult(statement='match(p:Actor)-[r:参演]->(m:Movie) where p.name="李连杰" return m.title',value='m.title'):
        print(result,type(result))

    print('*'*100)

    for result in cns.getSearchResult(statement='match(p:Actor)-[r:参演]->(m:Movie) where p.name="李连杰" return m.rating',value='m.rating'):
        print(result,type(result))

    '''
    The Mummy: Tomb of the Dragon Emperor <class 'str'>
    南北少林 <class 'str'>
    投名状 <class 'str'>
    Gong Shou Dao <class 'str'>
    Ultimate Fights from the Movies <class 'str'>
    Eastern Heroes: The Video Magazine - Volume 2 <class 'str'>
    龙在天涯 <class 'str'>
    黄飞鸿之二男儿当自强 <class 'str'>
    Top Fighter <class 'str'>
    黄飞鸿之三狮王争霸 <class 'str'>
    Unleashed <class 'str'>
    Romeo Must Die <class 'str'>
    The One <class 'str'>
    Cause: The Birth of Hero <class 'str'>
    给爸爸的信 <class 'str'>
    Hong Xi Guan: Zhi Shao Lin wu zu <class 'str'>
    Zhong hua ying xiong <class 'str'>
    Shao Lin xiao zi <class 'str'>
    黄飞鸿之铁鸡斗蜈蚣 <class 'str'>
    方世玉 <class 'str'>
    龙门飞甲 <class 'str'>
    Inferno: The Making of 'The Expendables' <class 'str'>
    黑侠 <class 'str'>
    笑傲江湖II东方不败 <class 'str'>
    封神传奇 <class 'str'>
    Kiss of the Dragon <class 'str'>
    黄飞鸿之西域雄狮 <class 'str'>
    Chop Socky: Cinema Hong Kong <class 'str'>
    Jing wu ying xiong <class 'str'>
    Cradle 2 the Grave <class 'str'>
    Dragons of the Orient <class 'str'>
    Zhong Nan Hai bao biao <class 'str'>
    倚天屠龙记之魔教教主 <class 'str'>
    Fong Sai Yuk juk jaap <class 'str'>
    The Forbidden Kingdom <class 'str'>
    白蛇传说 <class 'str'>
    Sat sau ji wong <class 'str'>
    不二神探 <class 'str'>
    英雄 <class 'str'>
    霍元甲 <class 'str'>
    Zhong hua wu shu <class 'str'>
    海洋天堂 <class 'str'>
    黄飞鸿 <class 'str'>
    太极张三丰 <class 'str'>
    Lethal Weapon 4 <class 'str'>
    Shao Lin Si <class 'str'>
    龙行天下 <class 'str'>
    War <class 'str'>
    少林真功夫 <class 'str'>
    Mao xian wang <class 'str'>
    The Expendables 2 <class 'str'>
    The Expendables <class 'str'>
    鼠胆龙威 <class 'str'>
    建国大业 <class 'str'>
    The Expendables 3 <class 'str'>
    ****************************************************************************************************
    5.1999998093 <class 'float'>
    6.8000001907 <class 'float'>
    6.3000001907 <class 'float'>
    7.0 <class 'float'>
    4.8000001907 <class 'float'>
    0.0 <class 'float'>
    5.5999999046 <class 'float'>
    7.1999998093 <class 'float'>
    7.0 <class 'float'>
    6.6999998093 <class 'float'>
    6.5999999046 <class 'float'>
    6.0 <class 'float'>
    5.6999998093 <class 'float'>
    8.0 <class 'float'>
    5.8000001907 <class 'float'>
    6.3000001907 <class 'float'>
    5.6999998093 <class 'float'>
    6.1999998093 <class 'float'>
    5.4000000954 <class 'float'>
    7.0999999046 <class 'float'>
    5.9000000954 <class 'float'>
    8.0 <class 'float'>
    5.9000000954 <class 'float'>
    6.9000000954 <class 'float'>
    5.0999999046 <class 'float'>
    6.4000000954 <class 'float'>
    5.6999998093 <class 'float'>
    6.8000001907 <class 'float'>
    7.4000000954 <class 'float'>
    5.8000001907 <class 'float'>
    0.0 <class 'float'>
    6.4000000954 <class 'float'>
    6.8000001907 <class 'float'>
    6.5 <class 'float'>
    6.3000001907 <class 'float'>
    5.5999999046 <class 'float'>
    6.1999998093 <class 'float'>
    4.5 <class 'float'>
    7.3000001907 <class 'float'>
    7.3000001907 <class 'float'>
    0.0 <class 'float'>
    7.0999999046 <class 'float'>
    7.4000000954 <class 'float'>
    7.0 <class 'float'>
    6.3000001907 <class 'float'>
    7.1999998093 <class 'float'>
    5.5999999046 <class 'float'>
    6.0 <class 'float'>
    8.0 <class 'float'>
    5.8000001907 <class 'float'>
    6.0999999046 <class 'float'>
    6.0 <class 'float'>
    5.5999999046 <class 'float'>
    4.9000000954 <class 'float'>
    6.0999999046 <class 'float'>
    '''