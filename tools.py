# coding=utf8
## 工具函数
import os,json

def printMenu(menuDict):
    '''
    菜单选项打印函数
    :param menuDict:
    :return:
    '''
    print('*' * 50)
    for k, v in menuDict.items():
        print('%s %s'%(k,v))
    print('输入 对应选项前的数字 回车即可执行操作')
    print('*' * 50)
    c = input('那么，What can i do for you? Tell me:')
    return c

def cmdRuner(comm,readList=False):
    '''
    命令执行函数
    :param comm:需要运行的命令
    :param readList:返回结果控制，为真时 return 结果为列表类型，为假时为字符串类型
    :return: 执行命令后翻回的结果
    '''
    result = os.popen(comm)
    if readList:
        return result.readlines()
    else:
        return result.read()