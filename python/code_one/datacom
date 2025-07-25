#导入python标准库
import time
from threading import Thread
import re
#导入第三方库
import paramiko
from ncclient import manager
#导入自定义py
import database as dt


class Switch:
    def __init__(self):
        #再构造函数中.提前预加载需要使用的正则表达式,节约系统资源
        self.pattern = {dev: re.compile(pat['re']) for dev,pat in dt.comist.items()}

    def get_ssh(self) -> paramiko.SSHClient:
        #创建获取ssh连接的方法
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #从配置文件中获取ssh连接信息,避免在主程序中输入,避免硬编码,并返回ssh连接
        client.connect(**dt.user_info['ssh'])
        return client

    def check_status(self) -> str:
        #获取ssh连接,并打开命令行会话通道,通过证则表达式匹配命令并返回交换机的状态信息
        vty = self.get_ssh().invoke_shell()
        vty.send('sc 0 t \n')
        while True:
            for dev,com in dt.comist.items():
                vty.send(com['command'] + '\n')
                time.sleep(0.5)
                out = self.pattern[dev].findall(vty.recv(65535).decode('utf-8'))
                res = 'fan is all ' if dev == 'fan' and not out else out
                print(f'{dev}:{res}')
            time.sleep(60 * 5)

    def download(self) -> str:
        #获取ssh连接,并打开sftp会话通道,通过sftp下载交换机的配置文件,并返回下载结果
        while True:
            with self.get_ssh() as sftp:
                file = sftp.open_sftp()
                file.get('vrpcfg.cfg',time.strftime('%Y_%m_%d_%H_%M_%S') + '_meiui.cfg')
                print('下载成功')
            time.sleep(60 * 60 * 24)

    def netconf(self) -> str:
        #获取netconf连接,并通过netconf发送定义好的配置
        with manager.connect(**dt.user_info['net_user']) as conn:
            for xml in dt.netxml.values():
                print(conn.edit_config(target='running', config=xml))

    def run_Tread(self) -> None:
        #创建并启动线程,分别执行检查交换机状态,下载配置文件,和发送netconf配置
        self.netconf()
        Thread(target=self.check_status).start()
        Thread(target=self.download).start()

if __name__ == '__main__':
    switch = Switch()
    switch.run_Tread()
