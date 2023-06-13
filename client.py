import socket
from ser import Ser


class Client(Ser):
    command = 0

    def __init__(self):
        self._addr = (self._host_ip, self._port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self._addr)

    def send_request(self, msg):
        message = msg.encode(self._frmt)
        msg_len = len(message)
        send_len = str(msg_len).encode(self._frmt)
        send_len += b' ' * (self._header-len(send_len))
        self.client.send(send_len)
        self.client.send(message)

    def input_cmd(self):
        self.command = int(input())


cli = Client()
cli.send_request("hi")
