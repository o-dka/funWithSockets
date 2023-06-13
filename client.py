import socket

header = 64
host = "localhost"
diss_msg = "!DISCONNECT"
port = 5050
host_ip = '127.0.1.1'
addr = (host_ip, port)
frmat = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)


def send_request(msg):
    message = msg.encode(frmat)
    msg_len = len(message)
    send_len = str(msg_len).encode(frmat)
    send_len += b' ' * (header-len(send_len))
    client.send(send_len)
    client.send(message)


send_request("hi")
