from channels.generic.websocket import WebsocketConsumer

socket_list = []


class ChatService(WebsocketConsumer):
    def connect(self):
        self.accept()
        socket_list.append(self)

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        for ws in socket_list:
            ws.send(text_data)

    def disconnect(self, code):
        print("websocket断开连接")
