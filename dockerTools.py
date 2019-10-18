# coding=utf8
# @Time    : 2019/10/14 0:44
# @project: easyBilibiliLive.py
# @FileName: cronTools.py
# @Software: PyCharm

# docker 操作函数
from tools import *
def runBTL(userName,userPW,dockerName,Backstage=True):
    '''
    BTL启动器
    :param userName: B站登陆名
    :param userPW: B站用户密码
    :param Backstage: 是否后台运行，默认后台运行
    :return: 返回整理的docker命令
    '''

    # 去除特殊字符，只保留汉字，字母、数字
    import re
    sub_str = re.sub(u"([^\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", dockerName)

    if Backstage:   # 是否后台运行
        comm = "sudo docker run --name='{dockerName}' -itd --rm -e USER_NAME={userName} -e USER_PASSWORD={userPW} zsnmwy/bilibili-live-tools".format(dockerName=sub_str,userName=userName,userPW=userPW)
    else:
        comm = "sudo docker run --name='{dockerName}' -it --rm -e USER_NAME={userName} -e USER_PASSWORD={userPW} zsnmwy/bilibili-live-tools".format(dockerName=sub_str,userName=userName,userPW=userPW)

    return comm


def getDockerName():
    # 获取docker 容器的名字
    res = cmdRuner(r"docker ps --format '{{.ID}}\t{{.Image}}\t{{.Names}}'")
    temp = {}
    if res:
        for line in res.splitlines():
            if 'zsnmwy/bilibili-live-tools' in line:
                temp[line.split()[2]] = line.split()[0]
    return temp