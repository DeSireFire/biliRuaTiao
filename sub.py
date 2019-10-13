# coding=utf8
# from tools import *
from dockerTools import *

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