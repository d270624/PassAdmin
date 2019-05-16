from channels.generic.websocket import WebsocketConsumer
from django.http.request import QueryDict
from index.tools.webssh import *
from index.models import PassWord


class WebSSH(WebsocketConsumer):
    message = {'status': 0, 'message': None}
    """
    status:
        0: ssh 连接正常, websocket 正常
        1: 发生未知错误, 关闭 ssh 和 websocket 连接

    message:
        status 为 1 时, message 为具体的错误信息
        status 为 0 时, message 为 ssh 返回的数据, 前端页面将获取 ssh 返回的数据并写入终端页面
    """

    def connect(self):
        try:
            self.accept()
            query_string = self.scope['query_string']
            connet_argv = QueryDict(query_string=query_string, encoding='utf-8')
            webuser = connet_argv.get('user')
            id = connet_argv.get('id')
            host = PassWord.objects.get(uid=int(id))
            width = connet_argv.get('width')
            height = connet_argv.get('height')
            width = int(width)
            height = int(height)
            self.ssh = webssh_socket(websocker=self, message=self.message, webuser=webuser, host=host, width=width,
                                     height=height)
        except Exception as e:
            self.message['status'] = 1
            self.message['message'] = str(e)
            message = json.dumps(self.message)
            self.send(message)
            self.close()

    def disconnect(self, close_code):
        try:
            self.ssh.close()
        except:
            pass

    def receive(self, text_data=None, bytes_data=None):  # 每次都执行接收网页发过来的json数据
        data = json.loads(text_data)
        if type(data) == dict:
            status = data['status']
            if status == 0:
                data = data['data']
                self.ssh.shell(data)
            else:
                cols = data['cols']
                rows = data['rows']
                self.ssh.resize_pty(cols=cols, rows=rows)
