# -*- coding: utf-8 -*-
# @Time    : 2019/5/4 16:10
# @Author  : Weiyang
# @File    : MyExceptionError.py
'''
我们自定义的程序中的异常
'''

class MyExceptionError(Exception):
    '自定义异常,方便排查问题'
    def __init__(self,exceptionInformation):
        super().__init__(self) # 初始化父类
        self.exceptionInformation = exceptionInformation # 异常信息

    def __str__(self):
        return self.exceptionInformation

if __name__ == '__main__':
    try:
        raise MyExceptionError('我的异常')
    except MyExceptionError as e:
        print(e) # 打印异常

    '''
    我的异常
    '''