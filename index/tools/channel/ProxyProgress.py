from channels.generic.websocket import WebsocketConsumer
import json
from index.tools.channel.Process_global import *
import time


class logs(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.close()

    def receive(self, text_data=None, bytes_data=None):  # 每次都执行接收网页发过来的json数据
        data = json.loads(text_data)
        filename = data.get('filename')
        while 1:
            Process = ProcessStatus.get(filename)
            if Process is None:
                continue
            if '100.00%' in Process:
                self.send(text_data=Process)
                ProcessStatus[filename] = ''
                break
            self.send(text_data=Process)
            time.sleep(0.1)
        self.close()
