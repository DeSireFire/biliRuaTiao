# coding=utf8
# @Time    : 2019/10/14 0:44
# @project: easyBilibiliLive.py
# @FileName: cronTools.py
# @Software: PyCharm
from tools import *

def crontabADD(crMins='*',crHours='*',crDays='*',crMouDays='*',crWeeks='*',yourComm='pwd'):
    '''
    crontab命令构造
    https://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/crontab.html
    :param crMins: 字符串，例：每小时的第3和第15分钟执行 3，15
    :param crHours: 字符串，例：每天的第3和第15小时执行 3，15。每天3到15小时 3-15
    :param crDays: 字符串，例子：每天执行 *。每隔两天执行 */2
    :param crMouDays: 字符串，例子：每月1、10、22日执行 1,10,22。
    :param crWeeks: 字符串，例子：每周日执行 0，其他以此类推到0~6，周日为一周第一天。
    :param yourComm: 字符串，要crontab控制执行的命令
    :return:
    '''
    comm = "{crMins} {crHours} {crDays} {crMouDays} {crWeeks} {yourComm}".format(
        crMins=crMins, crHours=crHours, crDays=crDays, crMouDays=crMouDays, crWeeks=crWeeks, yourComm=yourComm
    )
    return comm


def crontabFile(commList,startFile=False):
    # 读取crontab
    temp = cmdRuner('crontab -l',True)
    for ft in temp: # 筛选出宿主机原自带的crontab任务，添加到命令列表，避免执行crontab -r时是把无关的任务清除
        if 'DDScriptNum' not in ft:
            commList.append(ft)

    # 生成新的crontab定时任务文件
    import os
    if startFile:   # 是生成启动任务文件是关闭任务文件呢？
        filename = os.path.join(os.getcwd(),'ddStartcron')  # 是~
    else:
        filename = os.path.join(os.getcwd(), 'ddStopcron')  # 否~
    commList +=temp # 合并新旧定时任务
    commList = list(set(commList))  # 去重
    print(commList)
    # 文件存则覆盖，不存则创建
    with open(filename,'w') as f:
        for line in commList:
            if line and line != '\n':    # 如果不为空则写入
                f.write(line)

    # 检查文件是否修改成功
    import time
    if os.path.exists(filename):    #文件是否存在
        info = os.stat(filename)
        if time.time() - info.st_mtime < 60:    #修改时间是否在一分钟之内
            return True

    return False