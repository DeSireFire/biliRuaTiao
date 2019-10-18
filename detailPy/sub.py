# coding=utf8
# @Time    : 2019/10/14 0:44
# @project: easyBilibiliLive.py
# @FileName: cronTools.py
# @Software: PyCharm

# 次级操作函数

# from tools import *

from .dockerTools import *
from .cronTools import *

def run_docker():
    with open(os.path.join(os.getcwd(), 'config.json'), 'r') as f:
        info = json.load(fp=f)
    for user in info:  # 遍历多个用户
        for psN in range(0, info[user][1]):  # 用户多开次数
            dockerComm = runBTL(user, info[user][0], user + 'DDScriptNum%s' % psN)  # 构造启动docker命令
            dockerID = cmdRuner(dockerComm)[:12]
            print("账号：%s 第%s线程启动成功！ID:%s" % (user, psN + 1, dockerID))

def stop_docker():
    idList = getDockerName()  # 获取所有有关DD抢辣条的docker进程ID
    for idKey in idList:  # 遍历id 逐一关闭。时间较长
        comm = 'docker stop {CONTAINER_Name}'.format(CONTAINER_Name=idKey)
        print('正在关闭 %s ...' % (idKey))
        print('关闭进度: [{down}/{len}]'.format(
            list(idList.keys()).index(idKey) / len(idList.keys()),
            down=list(idList.keys()).index(idKey),
            len=len(idList.keys()),
        ))
        cmdRuner(comm)
    print('全部关闭完成！')

def print_docker_ps():
    # 格式化打印docker ps
    print(cmdRuner(r"docker ps --format 'table {{.ID}}\t{{.Image}}\t{{.Names}}'"))


def add_crontab_to_start():
    idList = getDockerName()  # 获取所有有关DD抢辣条的docker进程名称
    if not idList:
        print('没有发现在运行DD程序，请先启动再设置定时任务！')
        return
    import os
    with open(os.path.join(os.getcwd(), 'config.json'), 'r') as f:
        info = json.load(fp=f)

    comms = []
    for user in info:  # 遍历多个用户
        for psN in range(0, info[user][1]):  # 用户多开次数
            comm = runBTL(user, info[user][0], user + 'DDScriptNum%s' % psN)  # 构造启动docker命令
            crontabCommStart = crontabADD(crMins='30', crHours='9', crDays='*', crMouDays='*', crWeeks='*',
                                          yourComm=comm)  # 构造定时关闭任务命令
            comms.append(crontabCommStart)
    fstatus = crontabFile(comms, True)
    print(fstatus)
    if fstatus:
        print('定时任务文件创建...OK')
        print('查看当前已有定时任务 \n%s' % cmdRuner(r"crontab -l"))
        print('初始化 crontab 任务..')
        cmdRuner(r"crontab -r")
        print('重载 crontab 任务..')
        import os
        cmdRuner(r"crontab ddStartcron")
        print('查看重载后定时任务 \n%s' % cmdRuner(r"crontab -l"))
        print('一键设置所有DD抢辣条定时启动...OK')