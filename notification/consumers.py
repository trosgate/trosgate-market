from channels.generic.websocket import WebsocketConsumer


class NotifierConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self):
        pass