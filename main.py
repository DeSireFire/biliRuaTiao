# coding=utf8
# @Time    : 2019/9/29 14:53
# @FileName: controlBLT.py
# @Software: PyCharm


from detailPy.sub import *

## 工具函数


def choiceHandler(c):
    import os
    if c == 1:
        run_docker()

    elif c == 2:
        stop_docker()

    elif c == 3:
        print_docker_ps()

    elif c == 4:
        add_crontab_to_start()


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
        print('操作完毕，再如输入一次 python3 main.py 运行我吧？')
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
