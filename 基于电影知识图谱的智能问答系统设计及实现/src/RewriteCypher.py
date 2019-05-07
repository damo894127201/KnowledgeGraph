# -*- coding: utf-8 -*-
# @Time    : 2019/5/5 9:37
# @Author  : Weiyang
# @File    : RewriteCypher.py

'''
改写Cypher语句，即将我们在配置文件中预定的Cypher语句里的占位符填充上实际值
输入：待改写的Cypher语句，按顺序排列的每个占位符的实际值
输出：填充上实际值的Cypher语句
'''

from MyExceptionError import *
import traceback

class RewriteCypher(object):
    '改写Cypher类'
    def __init__(self):
        pass

    def run(self,statement,slots,slot_values):
        '''statement: 待改写的Cypher语句,例如: match(m:Movie) where m.title="%s" return m.rating
        slots: 按顺序排列的槽位标记列表,例如[nm,nnt,ng,x,...]
        slot_values: 槽位标记与实际值的映射字典，例如：
        {nnt:[word1,word2,..],ng:[word1,word2,..],nm:[word1,word2,..],x:[word1,word2,..]}'''
        placeholder = [] # 用于存储槽位实际值的占位符列表
        # 遍历槽位标记列表
        for slot in slots:
            # 判断槽位类别,x槽位需要特殊处理
            if slot == 'x':
                # 判断当前槽位标记与实际值的映射字典中是否为空
                if slot_values[slot] != []:
                    temp = slot_values[slot] # 实际值列表
                    placeholder.append(float(temp[0])) # 将列表中第一个值加入占位符列表
                    del temp[0] # 列表头部元素已经用过，当删除
                    slot_values[slot] = temp
                    continue
                else:
                    # 当前槽位对应的实际值没有了，则抛出槽位实际值不足的异常
                    '''
                    try:
                        raise MyExceptionError('当前槽位没有对应的实际值，请查看输入slots和slot_values的槽位是否相等！')
                    except MyExceptionError as e:
                        print(e)
                        print(traceback.format_exc()) #打印堆栈信息
                    finally:
                        return None
                    '''
                    return None

            if slot_values[slot] != []:
                temp = slot_values[slot]
                placeholder.append(temp[0])
                del temp[0]
                slot_values[slot] = temp
            else:
                # 当前槽位对应的实际值没有了，则抛出槽位实际值不足的异常
                '''
                try:
                    raise MyExceptionError('当前槽位没有对应的实际值，请查看输入slots和slot_values的槽位是否相等！')
                except MyExceptionError as e:
                    print(e)
                    print(traceback.format_exc())  # 打印堆栈信息
                finally:
                    return None
                '''
                return None

        return statement%tuple(placeholder)

if __name__ == '__main__':
    rc = RewriteCypher()

    statement = 'match(p:Actor)-[r:参演]->(m:Movie) where p.name="%s" and m.rating >= %.1f return m.title'
    slots = ['nnt','x']
    slot_values = {'nnt':['刘德华'],'x':['7.5']}
    result = rc.run(statement,slots,slot_values)
    print(result)
    '''
    match(p:Actor)-[r:参演]->(m:Movie) where p.name="刘德华" and m.rating >= 7.5 return m.title
    '''

    print('*'*50)

    statement = 'match(p1:Actor)--(m:Movie)--(p2:Actor) where p1.name="%s" and p2.name="%s" return m.title'
    slots = ['nnt','nnt']
    slot_values = {'nnt':['刘德华','周润发']}
    result = rc.run(statement, slots, slot_values)
    print(result)
    '''
    match(p1:Actor)--(m:Movie)--(p2:Actor) where p1.name="刘德华" and p2.name="周润发" return m.title
    '''

    print('*'*50)

    statement = 'match(p1:Actor)--(m:Movie)--(p2:Actor) where p1.name="%s" and p2.name="%s" return m.title'
    slots = ['nnt', 'nnt']
    slot_values = {'nnt': ['刘德华']}
    result = rc.run(statement, slots, slot_values)
    print(result)
    '''
    当前槽位没有对应的实际值，请查看输入slots和slot_values的槽位是否相等！
    Traceback (most recent call last):
      File "H:/MyNotes/知识图谱学习笔记/项目/基于电影知识图谱的智能问答系统/src/RewriteCypher.py", line 53, in run
        raise MyExceptionError('当前槽位没有对应的实际值，请查看输入slots和slot_values的槽位是否相等！')
    MyExceptionError.MyExceptionError: 当前槽位没有对应的实际值，请查看输入slots和slot_values的槽位是否相等！
    '''