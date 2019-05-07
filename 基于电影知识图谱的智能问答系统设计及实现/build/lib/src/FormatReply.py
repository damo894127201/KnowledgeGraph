# -*- coding: utf-8 -*-
# @Time    : 2019/5/5 12:03
# @Author  : Weiyang
# @File    : FormatReply.py

'''
格式化输入
用途：格式化Neo4j查询结果
输入：一个可迭代的对象
输出：格式化后的字符串
'''

class FormatReply(object):
    '格式化输入'
    def __init__(self):
        pass

    def formatReply(self,iterator):
        '格式化可迭代对象,iterator:可迭代对象'
        reply = [] # 存储格式化后的结果
        for line in iterator:
            if type(line) == float:
                line = round(line,2) # 如果回复是float型，则保留2位小数位
                reply.append(line)
                continue
            reply.append(line.strip())
        # 如果reply为空，则返回None
        if reply == []:
            return None
        else:
            return '，'.join([str(i) for i in reply])

if __name__ == '__main__':
    fr = FormatReply()
    iters = ['a',3.256,'b']
    result = fr.formatReply(iters)
    print(result)
    '''
    a
    3.26
    b
    '''
    result = fr.formatReply([])
    print(result)
    '''
    None
    '''
