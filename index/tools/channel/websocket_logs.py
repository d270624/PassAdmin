from index.Rsa import *
from channels.generic.websocket import WebsocketConsumer
import paramiko
import socket
import threading
from index.forms import *
import logging
import json
mylog = logging.getLogger('django.server')
en = RsaChange()


class logs(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.getMessageStatus = False

    def disconnect(self, close_code):
        self.chan.close()
        self.t.close()
        self.getMessageStatus = True
        self.close()

    def xx(self):
        for x in range(2):
            self.chan.recv(1024).decode('utf-8')
        while True:
            if self.getMessageStatus:
                break
            try:
                ret = self.chan.recv(4096).decode('utf-8')
                self.send(text_data=ret)
            except socket.timeout:
                self.t.close()
                self.close()

    def receive(self, text_data=None, bytes_data=None):  # 每次都执行接收网页发过来的json数据
        try:
            data = json.loads(text_data)
            uid = data['uid']
            obj_uid = data['obj_uid']
            server = PassWord.objects.get(uid=int(uid))  # 获取服务器信息
            obj = Object.objects.get(uid=int(obj_uid))  # 获取项目日志路径
            self.t = paramiko.Transport((server.ip, server.port))
            self.t.connect(username=server.user, password=en.decrypt(server.password))
            self.chan = self.t.open_session()
            # 设置会话超时时间
            self.chan.settimeout(300)
            # 打开远程的terminal
            self.chan.get_pty()
            # 激活terminal
            self.chan.invoke_shell()
            self.chan.send('tail -f ' + obj.obj_log + '\n')
            mylog.info(server)
            mylog.info(obj.obj_log)
            self.task = threading.Thread(target=self.xx)
            self.task.start()
        except:
            pass
