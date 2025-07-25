import re
import time
import threading

import paramiko
from ncclient import manager

import database


class Switch:
    def __init__(self):
        self.pattern = {dev:re.compile(pat['re']) for dev,pat in database.comist.items()}

    def get_ssh(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('10.1.0.6',22,'python','Huawei@123')
        return client

    def check_status(self):
        vty = self.get_ssh().invoke_shell()
        vty.send('sc 0 t \n')
        while True:
            for dev,com in database.comist.items():
                vty.send(com['command'] + '\n')
                time.sleep(1)
                out = self.pattern[dev].findall(vty.recv(65535).decode('utf-8'))
                res = '已经全部损坏' if dev == 'fan' and not out else out
                print(f'{dev}:{res}')
            time.sleep(5 * 60)

    def download(self):
        while True:
            with self.get_ssh() as files:
                sftp = files.open_sftp()
                sftp.get('vrpcfg.zip',time.strftime('%Y_%m_%d_%H_%M_%S_') + 'T1_AGG1.zip')
            print('下载成功')
            time.sleep(24 * 60 * 60)

    def netconf(self):
        with manager.connect(host='10.1.0.6', port=830, username='netconf', password='Huawei@123',
                            hostkey_verify=False, allow_agent=False, device_params={'name':'huawei'}
                             ) as con:
            for xml in database.netxml.values():
                print(con.edit_config(target='running', config=xml))

    def run_th(self):
        self.netconf()
        threading.Thread(target=self.download).start()
        threading.Thread(target=self.check_status).start()


if __name__ == '__main__':
    switch = Switch()
    switch.run_th()
