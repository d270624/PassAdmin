from channels.generic.websocket import WebsocketConsumer
import json
import logging
import time
import os

mylog = logging.getLogger('django.server')


class logs(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.close()

    def receive(self, text_data=None, bytes_data=None):  # 每次都执行接收网页发过来的json数据
        data = json.loads(text_data)
        filename = data.get('filename')
        time.sleep(1)
        with open("log/" + filename + '.txt') as file_:
            # Go to the end of file
            file_.seek(0, 2)
            while True:
                curr_position = file_.tell()
                line = file_.readline()
                if not line:
                    file_.seek(curr_position)
                else:
                    self.send(text_data=line)
                    if '100' in line:
                        self.send(text_data='success')
                        break
        os.remove('log/' + filename + '.txt')
        self.close()
