import requests
import os
import time
import warnings
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse

# 忽略 InsecureRequestWarning
warnings.simplefilter("ignore", InsecureRequestWarning)
# 登录面板
def LoginPanel(hostname, username, password):
    hostname_number = hostname.split('.')[0].replace('s', '')
    host = f'https://panel{hostname_number}.serv00.com/login/'
    time.sleep(2)
    headers = {
        'Referer' : host,
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    msg = ''
    try:
        res = requests.get(host, verify=False)
        csrftoken = res.cookies['csrftoken']
        data = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': csrftoken,
        }
        res = requests.post(host, data=data,headers=headers,cookies=res.cookies,verify=False)
        if res.text.find('/logout/') != -1:
            msg = '✅面板登录成功'
        else:
            msg = '❌面板登录失败'
    except Exception as e:
        msg += f"❌面板登录异常: {e}"
    print(msg)
    return msg
        
# 登录ssh
def LoginSsh(hostname, username, password):
    import paramiko
    # 创建ssh对象
    with paramiko.SSHClient() as ssh:
        # 自动添加SSH密钥
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        msg = ''
        print('开始ssh连接')
        try:
            # 连接服务器
            ssh.connect(hostname=hostname, username=username, password=password)
            msg = '✅ssh连接成功\n开始执行查看ip命令'
            print('ssh连接成功')
            print('开始执行查看ip命令')
            
            # 执行命令
            stdin, stdout, stderr = ssh.exec_command("curl ifconfig.me")
            ip = stdout.read().decode()
            print(ip)
            msg += '\n✅IP:' + ip
        except Exception as e:
            print(f"SSH连接失败: {e}")
            msg += f"❌SSH连接失败: {e}"
        return msg
        
if __name__ == '__main__':
    # 从环境变量中获取服务器信息
    Serv00 = os.environ.get('Serv00')
    if Serv00 is None:
        print('没有找到服务器信息,请重新设置变量Serv00')
        os._exit(0)
    severs = Serv00.split(';')
    msgs = []
    for server in severs:
        serv = urlparse(f'http://{server}')
        hname = serv.hostname
        uname = serv.username
        passw = serv.password
        msg = f'开始执行服务器: {uname}@{hname}\n'
        try:
            msg += LoginPanel(hname, uname, passw)
            msg += '\n' + LoginSsh(hname, uname, passw)
            msgs.append(msg)
        except Exception as e:  # 捕获所有异常
            print(f"执行服务器{uname}@{hname}时发生异常: {e}")
            msgs.append(f"\n❌执行服务器时发生异常: {e}")

    QLAPI.notify('Serv00保活通知', ('\n\n').join(msgs))

