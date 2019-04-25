import paramiko
from threading import Thread
from index.tools.tools import get_key_obj
import socket
import json
import time
import os


class SSH:
    def __init__(self, websocker, message, webuser, host):
        self.websocker = websocker
        self.message = message
        self.status = 1
        try:
            os.mkdir('log/' + webuser)
        except:
            pass
        self.log = open('log/' + webuser + '/' + host + '.log', 'a')
        self.log.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "    login\n")
        self.log.flush()
        self.m = ''

    def connect(self, host, user, password, pkey=None, port=22, timeout=30,
                term='xterm', pty_width=80, pty_height=24):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if pkey:
                key = get_key_obj(paramiko.RSAKey, pkey_obj=pkey, password=password) or \
                      get_key_obj(paramiko.DSSKey, pkey_obj=pkey, password=password) or \
                      get_key_obj(paramiko.ECDSAKey, pkey_obj=pkey, password=password) or \
                      get_key_obj(paramiko.Ed25519Key, pkey_obj=pkey, password=password)

                ssh_client.connect(username=user, hostname=host, port=port, pkey=key, timeout=timeout)
            else:
                password = password.replace('amp;', '')
                ssh_client.connect(username=user, password=password, hostname=host, port=port, timeout=timeout)

            self.transport = ssh_client.get_transport()
            self.channel = self.transport.open_session()
            self.channel.get_pty(term=term, width=pty_width, height=pty_height)
            self.channel.invoke_shell()

            for i in range(2):
                # time.sleep(0.05)
                recv = self.channel.recv(1024).decode('utf-8')
                self.message['status'] = 0
                self.message['message'] = recv
                message = json.dumps(self.message)
                self.websocker.send(message)

        except socket.timeout as e:
            self.message['status'] = 1
            self.message['message'] = 'ssh 连接超时'
            message = json.dumps(self.message)
            self.websocker.send(message)
            self.websocker.close()
        except Exception as e:
            self.message['status'] = 1
            self.message['message'] = str(e)
            message = json.dumps(self.message)
            self.websocker.send(message)
            self.websocker.close()

    def resize_pty(self, cols, rows):
        self.channel.resize_pty(width=cols, height=rows)

    def django_to_ssh(self, data):
        try:
            self.channel.send(data)
            # 如果用户按了回车键才回发送，在按回车键之前的操作全部放在一个变量中
            if data == '\r':
                if len(self.m):
                    self.log.write(self.m + '\n')
                    self.log.flush()
                    self.m = ''
            elif data == '\t' or '' in data:  # 这个第一个空白代表esc键，第二个是ETX
                pass
            elif data == '':  # 这个空白代表删除键
                self.m = self.m[:-1]
            elif data == '':
                self.m = ''
            else:
                self.m = self.m + data
        except:
            self.close()

    def websocket_to_django(self):
        while True:
            try:
                self.status = 0
                data = self.channel.recv(1024).decode('utf-8')
                if not data:
                    self.status = 1
                    break
                self.message['status'] = 0
                self.message['message'] = data  # 将服务器返回的信息传输到前端，用户输入了exit以后内存就会释放
                message = json.dumps(self.message)
                self.websocker.send(message)
            except UnicodeDecodeError:
                pass
            except:
                self.close()

    def close(self):
        try:
            self.channel.send('')
        except:
            pass
        self.log.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "    logout\n")
        self.log.flush()
        self.log.close()
        self.message['status'] = 1
        self.message['message'] = '关闭连接'
        message = json.dumps(self.message)
        self.websocker.send(message)
        self.channel.close()
        self.transport.close()
        self.websocker.close()

    def shell(self, data):
        Thread(target=self.django_to_ssh, args=(data,)).start()
        if self.status == 1:  # 等于1的时候执行线程
            Thread(target=self.websocket_to_django).start()
