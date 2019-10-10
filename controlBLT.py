# coding=utf8
# @Time    : 2019/9/29 14:53
# @FileName: controlBLT.py
# @Software: PyCharm

from tools import *

## 工具函数


def getDockerName():
    # 获取docker 容器的名字
    res = cmdRuner(r"docker ps --format '{{.ID}}\t{{.Image}}\t{{.Names}}'")
    temp = {}
    if res:
        for line in res.splitlines():
            if 'zsnmwy/bilibili-live-tools' in line:
                temp[line.split()[2]] = line.split()[0]
    return temp

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
        comm = "docker run --name='{dockerName}' -itd --rm -e USER_NAME={userName} -e USER_PASSWORD={userPW} zsnmwy/bilibili-live-tools".format(dockerName=sub_str,userName=userName,userPW=userPW)
    else:
        comm = "docker run --name='{dockerName}' -it --rm -e USER_NAME={userName} -e USER_PASSWORD={userPW} zsnmwy/bilibili-live-tools".format(dockerName=sub_str,userName=userName,userPW=userPW)

    return comm

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
    # 文件存则覆盖，不存则创建
    with open(filename,'w') as f:
        for line in commList:
            if line:    # 如果不为空则写入
                f.write(line+'\n')

    # 检查文件是否修改成功
    import time
    if os.path.exists(filename):    #文件是否存在
        info = os.stat(filename)
        if time.time() - info.st_mtime < 60:    #修改时间是否在一分钟之内
            return True

    return False

def choiceHandler(c):
    import os
    if c == 1:
        with open(os.path.join(os.getcwd(),'config.json'), 'r') as f:
            info = json.load(fp=f)
        for user in info:   # 遍历多个用户
            for psN in range(0,info[user][1]):  # 用户多开次数
                dockerComm = runBTL(user, info[user][0],user+'DDScriptNum%s'%psN)  # 构造启动docker命令
                dockerID = cmdRuner(dockerComm)[:12]
                print("账号：%s 第%s线程启动成功！ID:%s"%(user,psN+1,dockerID))


    elif c == 2:
        idList = getDockerName()  # 获取所有有关DD抢辣条的docker进程ID
        for idKey in idList: # 遍历id 逐一关闭。时间较长
            comm = 'docker stop {CONTAINER_Name}'.format(CONTAINER_Name=idKey)
            print('正在关闭 %s ...'%(idKey))
            print('关闭进度: [{down}/{len}]'.format(
                list(idList.keys()).index(idKey)/len(idList.keys()),
                down=list(idList.keys()).index(idKey),
                len=len(idList.keys()),
            ))
            cmdRuner(comm)
        print('全部关闭完成！')

    elif c == 3:
        # 格式化打印docker ps
        print(cmdRuner(r"docker ps --format 'table {{.ID}}\t{{.Image}}\t{{.Names}}'"))


    elif c == 4:
        idList = getDockerName()  # 获取所有有关DD抢辣条的docker进程名称
        if not idList:
            print('没有发现在运行DD程序，请先启动再设置定时任务！')
            return

        with open(os.path.join(os.getcwd(),'config.json'), 'r') as f:
            info = json.load(fp=f)

        comms = []
        for user in info:   # 遍历多个用户
            for psN in range(0,info[user][1]):  # 用户多开次数
                comm = runBTL(user, info[user][0],user+'DDScriptNum%s'%psN)  # 构造启动docker命令
                crontabCommStart = crontabADD(crMins='30', crHours='9', crDays='*', crMouDays='*', crWeeks='*',yourComm=comm)  # 构造定时关闭任务命令
                comms.append(crontabCommStart)
        fstatus = crontabFile(comms,True)
        print(fstatus)
        if fstatus:
            print('定时任务文件创建...OK')
            print('查看当前已有定时任务 \n%s'%cmdRuner(r"crontab -l"))
            print('初始化 crontab 任务..')
            cmdRuner(r"crontab -r")
            print('重载 crontab 任务..')
            import os
            cmdRuner(r"crontab ddStartcron")
            print('查看重载后定时任务 \n%s'%cmdRuner(r"crontab -l"))
            print('一键设置所有DD抢辣条定时启动...OK')


    elif c == 5:
        idList = getDockerName()  # 获取所有有关DD抢辣条的docker进程ID
        if not idList:
            print('没有发现在运行DD程序，请先启动再设置定时任务！')
            return
        comms = []
        for idKey in idList: # 遍历id
            comm = 'docker stop {CONTAINER_Name}'.format(CONTAINER_Name=idKey)
            crontabCommStop = crontabADD(crMins='30', crHours='2', crDays='*', crMouDays='*', crWeeks='*',yourComm=comm)  # 构造定时关闭任务命令
            comms.append(crontabCommStop)
        fstatus = crontabFile(comms)
        print(fstatus)
        if fstatus:
            print('定时任务文件创建...OK')
            print('查看当前已有定时任务 \n%s'%cmdRuner(r"crontab -l"))
            print('初始化 crontab 任务..')
            cmdRuner(r"crontab -r")
            print('重载 crontab 任务..')
            cmdRuner('crontab ddStopcron')
            print('查看重载后定时任务 \n%s'%cmdRuner(r"crontab -l"))
            print('一键设置所有DD抢辣条定时启动...OK')


    elif c == 6:
        # 读取文件
        with open(os.path.join(os.getcwd(),'config.json'), 'r') as f:
            info = json.load(fp=f)
        print('已存用户名列表如下：')
        for i in info:
            print(i)

    elif c == 7:
        while True:
            user = input('请输入你的B站账号：')
            pwd = input('请输入你的B站账号密码：')

            status = input('确定上述信息输入无误吗？(输入 1 为 确定！,其他为 否)：')
            if status == '1':
                break
        # 修改config文件
        with open(os.path.join(os.getcwd(),'config.json'), 'r') as f:
            info = json.load(fp=f)
        info.update({user: [pwd, 2]})
        with open(os.path.join(os.getcwd(), 'config.json'), 'w') as f:
            json.dump(info, f)

    elif c == 8:
        # 读取文件
        with open(os.path.join(os.getcwd(),'config.json'), 'r') as f:
            info = json.load(fp=f)
        print('已存用户名列表如下：')
        for i in info:
            print(i)
        delD = input('你要删除的用户名是(别打错了哟)：')
        if delD in info.key():
            del info[delD]
            print('%s 已经删除。')
            print('当前用户名列表如下：')
            for i in info:
                print(i)
            print('保存修改后的信息...')
            with open(os.path.join(os.getcwd(), 'config.json'), 'w') as f:
                json.dump(info, f)
            print('保存修改后的信息...ok')

def menu():
    menuDict = {
        1:'一键启动所有DD抢辣条',
        2:'一键退出所有DD抢辣条',
        3:'显示所有在运行DD抢辣条进程',
        4:'一键设置所有DD抢辣条定时启动',
        5:'一键设置所有DD抢辣条定时关闭',
        6:'查看已存B站账号',
        7:'添加新的B站账号',
        8:'删除已存的B站账号',
        0:'退出工具',
    }
    if not os.path.exists(os.path.join(os.getcwd(),'config.json')):
        print('未发现配置文件 config.py ，可能为第一次启动')
        while True:
            user = input('请输入你的B站账号：')
            pwd = input('请输入你的B站账号密码：')
            psNum = int(input('该账号多开进程数（如果你看不懂，你就写 1 ）：'))

            status = input('确定上述信息输入无误吗？(输入 1 为 确定！,其他为 否)：')
            if status == '1':
                break
        # 创建config文件
        with open(os.path.join(os.getcwd(),'config.json'), 'w') as f:
            info = {user:[pwd, psNum]}
            json.dump(info, f)
        print('操作完毕，再如输入一次 python3 controlBLT.py 运行我吧？')
        return


    while True:

        c = printMenu(menuDict)

        try:
            c = int(c)
            if c not in menuDict.keys():
                raise RuntimeError
            break
        except:
            print('输入有误！')

    if c in [1,2,3,4,5,6,7,8]:    # 是否退出
        print('%s %s Start!' % (c, menuDict[c]))
        choiceHandler(c)
    else:
        pass


if __name__ == '__main__':
    menu()
# docker run -it --rm -e USER_NAME=1025212779@qq.com -e USER_PASSWORD=gannimei zsnmwy/bilibili-live-tools
