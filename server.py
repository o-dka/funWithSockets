import socket
import threading
import time
log_file = open("log.txt", 'a')

header = 64
host = "localhost"
diss_msg = "!DISCONNECT"
port = 5050
host_ip = socket.gethostbyname(socket.gethostname())
addr = (host_ip, port)
frmat = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)


def handle_client(conn, addr):
    print(f"[NEW CON] {addr} connected")

    conned = True
    while conned:
        msg_len = len(conn.recv(header).decode(frmat))
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(frmat)
            if msg == diss_msg:
                conned = False
            print(f"{addr} - {msg}")
    conn.close()


def start():
    print("[STARTING]")
    server.listen()
    print(f"Server is listening on {server}")
    while True:
        conn, addr = server.accept()
        try:
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[CONNECTIONS ACTIVE: ] {threading.active_count()-1}")
        except Exception as error:
            log_file.write(f"ERROR OCCURED AT {time.ctime()}")
            log_file.write(str(error))
            log_file.write("================================\n")
            log_file.close()
            exit(1)


start()
