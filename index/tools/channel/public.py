from channels.generic.websocket import WebsocketConsumer


class show(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.close()

    def receive(self, text_data=None, bytes_data=None):  # 每次都执行接收网页发过来的json数据
        try:
            self.send(text_data='11')
            # uid = text_data.split('|')[0]
            # obj_uid = text_data.split('|')[1]
        except:
            pass
