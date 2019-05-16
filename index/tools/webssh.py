# _*_coding:utf-8_*_
import paramiko
import socket
from paramiko.py3compat import u
import json
from threading import Thread
import time
import os
from index.Rsa import *

en = RsaChange()


class webssh_socket:
    def __init__(self, websocker, message, webuser, host, width=80, height=24):
        self.message = message
        self.websocker = websocker
        self.cmd_caches = []
        self.status = 1
        try:
            os.mkdir('log/' + webuser)
        except:
            pass
        if host.intranet_ip is None:
            ip = host.ip
        else:
            ip = host.intranet_ip
        self.log = open('log/' + webuser + '/' + ip + '.log', 'a')
        self.log.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "    login\n")
        self.log.flush()
        self.m = ''
        client = paramiko.SSHClient()
        try:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip,
                           host.port,
                           host.user,
                           en.decrypt(host.password),
                           timeout=30)
            self.chan = client.invoke_shell()
            self.chan.get_pty(term='xterm', width=width, height=height)
            time.sleep(0.5)
            recv = self.chan.recv(2048).decode('utf-8')
            self.message['status'] = 0
            self.message['message'] = recv
            message = json.dumps(self.message)
            self.websocker.send(message)
            self.cmd_caches.append('login')

        except socket.timeout:
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

    def recv(self):
        while True:
            try:
                self.status = 0
                x = u(self.chan.recv(1024).decode('utf-8'))
                if len(x) == 0:
                    self.status = 1
                    break
                self.message['status'] = 0
                self.message['message'] = x  # 将服务器返回的信息传输到前端，用户输入了exit以后内存就会释放
                message = json.dumps(self.message)
                self.websocker.send(message)
            except UnicodeDecodeError:
                pass
            except:
                self.close()

    def send(self, data):
        try:
            self.chan.send(data)
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

    def resize_pty(self, cols, rows):
        self.chan.resize_pty(width=cols, height=rows)

    def close(self):
        try:
            self.chan.send('')
        except:
            pass
        self.message['status'] = 1
        self.message['message'] = '关闭连接'
        message = json.dumps(self.message)
        self.websocker.send(message)
        self.chan.close()
        self.websocker.close()

    def shell(self, data):
        Thread(target=self.send, args=(data,)).start()
        if self.status == 1:  # 等于1的时候执行线程
            Thread(target=self.recv).start()
