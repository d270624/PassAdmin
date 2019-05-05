from channels.generic.websocket import WebsocketConsumer
from xmlrpc.client import ServerProxy
from index.models import supervisor
import json
import threading


class show(WebsocketConsumer):

    def connect(self):
        self.getMessageStatus = False
        self.accept()

    def disconnect(self, close_code):
        self.getMessageStatus = True
        self.close()

    def xx(self, server, name, tmp_var):
        while True:
            if self.getMessageStatus:
                break
            current = server.supervisor.tailProcessLog(name, 0, 0)  # 1005
            if current[1] != tmp_var:
                result = server.supervisor.tailProcessLog(name, 0, current[1] - tmp_var)
                self.send(result[0])
                tmp_var = current[1]

    def receive(self, text_data=None, bytes_data=None):  # 每次都执行接收网页发过来的json数据
        res = json.loads(text_data)
        name = res['name']
        id = res['id']
        try:
            res = supervisor.objects.get(id=int(id))
            if res.ip.intranet_ip is None:
                ip = res.ip.ip
            else:
                ip = res.ip.intranet_ip
            server = ServerProxy('http://' + res.user + ':' + res.password + '@' + ip + ':' + str(res.port) + '/RPC2')
            result = server.supervisor.tailProcessLog(name, 0, 1024)
            tmp_var = result[1]
            self.send(result[0])
            self.task = threading.Thread(target=self.xx, args=(server, name, tmp_var))
            self.task.start()
        except:
            pass
