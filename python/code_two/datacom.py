import re
import time
import threading
#导入Python标准库
import paramiko
from ncclient import manager
#导入python第三方库
import database
#导入自定义库,但是在这里的版本是只做参考的,如在这里的文件应该是config

class Switch:
    def __init__(self):
        self.pattern = {dev:re.compile(pat['re']) for dev,pat in database.comist.items()}
        #预先加载所需的正则表达式,避免后续调用重复加载,节约系统资源

    def get_ssh(self):
        #创建一个获取SSH会话的函数,避免重复创建SSH会话
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('10.1.0.6',22,'python','Huawei@123')
        #返回SSH客户端
        return client

    def check_status(self):
        vty = self.get_ssh().invoke_shell()
        #使用获取SS和会话的函数,创建命令行会话通道
        vty.send('sc 0 t \n')
        #输入参数,让交换机产生所有的命令输出,避免多按空格
        while True:
            for dev,com in database.comist.items():
                vty.send(com['command'] + '\n')
                #提取出命令,传入交换机并回车
                time.sleep(1)
                out = self.pattern[dev].findall(vty.recv(65535).decode('utf-8'))
                #从提前加载好的正则表达式字典中,提取出根据索引提取出所需的正则表达式,并匹配交换机输出的配置信息
                res = '已经全部损坏' if dev == 'fan' and not out else out
                print(f'{dev}:{res}')
            time.sleep(5 * 60)

    def download(self):
        #可以下载交换机的配置文件
        while True:
            with self.get_ssh() as files:
                #使用with上下文管理,的形式,可以保证使用完SS会话后自动关闭SSH会话
                sftp = files.open_sftp()
                #开启SFTP的方法,以便向交换机请求下载配置文件
                sftp.get('vrpcfg.zip',time.strftime('%Y_%m_%d_%H_%M_%S_') + 'T1_AGG1.zip')
                #下载所需的配置文件,time库的方法格式化下载时间,在考试中我遇到的是精确到天
            print('下载成功')
            time.sleep(24 * 60 * 60)

    def netconf(self):
        with manager.connect(host='10.1.0.6', port=830, username='netconf', password='Huawei@123',
                            hostkey_verify=False, allow_agent=False, device_params={'name':'huawei'}
                             ) as con:
                        #使用wIth上下文管理的形式,可以保证使用完netconf会话,自动关闭,对于方法中不能补全的参数,结合help文件夹中的知道食用更甚.
            for xml in database.netxml.values():
                #遍历config的value传入设备
                print(con.edit_config(target='running', config=xml))
                #使用edit_config的形式刷入配置,可以考虑,rpc方法,具体方法取决于个人,但是如果使用本方法,需要保证复制到这里的xml,复制到config标签即可.

    def run_th(self):
        #创建运行函数.多线程运行下载文件,和状态检测,以及netconf日志主机配置`
        self.netconf()
        threading.Thread(target=self.download).start()
        threading.Thread(target=self.check_status).start()


if __name__ == '__main__':
    switch = Switch()
    switch.run_th()
