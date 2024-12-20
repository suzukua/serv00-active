python脚本

功能如下：
1. 自动登录ssh后输出外网ip后退出
2. 自动登录web面板

设置青龙环境变量名称Serv00 内容为(服务器ip,账号,密码)格式如右边用小写逗号隔开:s15.serv00.com,username,password

依赖管理添加paramiko,requests,urllib3

![image](https://github.com/user-attachments/assets/f3d70777-377f-4ae1-85e1-c9363efc5b25)

脚本管理添加文件serv00.py代码：https://raw.githubusercontent.com/gooaclok819/serv00-active/refs/heads/main/serv00.py

![image](https://github.com/user-attachments/assets/dcc2393b-db5e-4fae-94ce-6286baef8335)

定时任务创建任务名称自定义,文件写serv00.py 定时规则3  0 * * * 我这里写的是12点3分执行,可以自定义

![image](https://github.com/user-attachments/assets/cfb47586-52c5-4ecb-bde8-0275b6449fae)
