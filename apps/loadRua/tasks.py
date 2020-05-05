# coding=utf8
# -*- coding: utf-8 -*-
# @Time    : 2020/5/4 18:52
# @Author  : RaXianch
# @project : biliRuaTiao.py
# @FileName: tasks.py
# @Software: PyCharm
# @github  :https://github.com/DeSireFire

# 导入数据模组
from .models import biliUser

# 引用定时调度
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

# 导入docker工具函数
from .dockerTools import cmdRuner
from .dockerTools import runBTL
from .dockerTools import getDockerName




# 实例化调度器
scheduler = BackgroundScheduler()


@register_job(scheduler, 'cron', id='dockerStart', hour=9, minute=13)
def dockerStart():
    users = list(biliUser.objects.all().values())  # [{'id': 1, 'buser': '1025212779@qq.com', 'bpw': 'zhaoritian'}]
    print(users)
    print('测试！')
    # 启动docker进程
    for user in users:  # 遍历多个用户
        dockerComm = runBTL(user["buser"], user["bpw"], user["buser"] + 'DDScriptNum')  # 构造启动docker命令
        dockerID = cmdRuner(dockerComm)[:12]
        print("账号：%s 线程启动成功！ID:%s" % (user["buser"], dockerID))


@register_job(scheduler, 'cron', id='dockerStop', hour=2, minute=30)
def dockerStop():
    # 停止docker进程
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


@register_job(scheduler, "interval", id='test', seconds=30)
def test():
    # 测试用定时任务
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

def main():
    # 开启定时工作
    try:
        # 实例化调度器
        scheduler = BackgroundScheduler()
        # 调度器使用DjangoJobStore()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # 设置定时任务，选择方式为interval，时间间隔为10s
        # 另一种方式为周一到周五固定时间执行任务，对应代码为：
        # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='8', minute='30', second='10',id='task_time')
        # @register_job(scheduler, "interval", seconds=10)

        register_events(scheduler)
        scheduler.start()
    except Exception as e:
        print(e)
        # 有错误就停止定时器
        scheduler.shutdown()
