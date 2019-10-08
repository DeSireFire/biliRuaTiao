# easyBilibiliLive
easyBilibiliLive,一个袖珍傻瓜式B站直播挂机小程序。

---
*重要说明*  

使用该控制脚本必须前置安装 docker、crontab、python3.*  
该脚本依赖于[bilibili-live-tools](https://github.com/Dawnnnnnn/bilibili-live-tools)项目  
感谢 Dawnnnnnn 大佬 开发了它。  

提供支持&联系我&增加功能？ => [Open a new issue](https://github.com/Dawnnnnnn/bilibili-live-tools)

---

1. 功能说明:
```bash
1:一键启动所有DD抢辣条
2:一键退出所有DD抢辣条
3:显示所有在运行DD抢辣条进程
4:一键设置所有DD抢辣条定时启动
5:一键设置所有DD抢辣条定时关闭
6:查看已存B站账号
7:添加新的B站账号
8:删除已存的B站账号
```

2. 环境说明:
```bash
python3+  
目前仅在Ubuntu18.04上测试运行过，一般来说Linux系统都可以部署使用。  
Win系统为尝试过。  
```

3. 使用方法说明:
安装：
```bash
git clone https://github.com/DeSireFire/easyBilibiliLive.git
```
使用： （根据提示输入账号密码和操作选项即可）
```bash
python3 controlBLT.py
```

4. 配置文件说明:
```bash
输入完B站账号密码，会生成一个配置文件 config.json 。  
该文件的重要程度与密码等同，不要发送给别人，这上面有你B站账号的重要信息。  
如果不需要它，请优先删除它。
```
