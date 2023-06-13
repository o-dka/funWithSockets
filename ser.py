import socket
import threading
import time


class Ser:
    __log_file = open("log.txt", 'a')
    connected_list = []
    _host_name = None
    _host_ip = socket.gethostbyname(socket.gethostname())
    diss_msg = "!DISSCONNECT"
    _header = 64
    _port = 5050
    _frmt = 'utf-8'
    _addr = None

    def __init__(self, host, sensors):
        self._host_name = host
        self._addr = (self._host_ip, self._port)
        self.sensors = []
        self.sensors = sensors

    def __disconnect_all(self):
        for _ in self.connected_list:
            _.close()

    def handler(self, conn, addr):
        print(f"[NEW CON] {addr} connected")
        conned = True
        while conned:
            msg_len = len(conn.recv(self._header).decode(self._frmt))
            if msg_len:
                msg_len = int(msg_len)
                msg = conn.recv(msg_len).decode(self._frmt)
                print(f"{addr} - {msg}")
                if msg == "ls":
                    for _ in self.sensors:
                        print(_.id, _.name)
                if msg[2:] == 'cd':
                    print(self.sensors[msg[4]].check_data())
                if msg == self.diss_msg:
                    conned = False
                    try:
                        self.connected_list.pop(
                            self.connected_list.index(addr))
                    except ValueError:
                        print("Connection terminated!")
                    finally:
                        break

        conn.close()

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self._addr)
        print("[STARTING]")
        self.server.listen()
        print(f"Server is listening on {self.server}")
        while True:
            conn, self._addr = self.server.accept()
            try:
                thr = threading.Thread(
                    target=self.handler, args=(conn, self._addr)
                )
                self.connected_list += self._addr
                thr.start()
                print(
                    f"[CONNECTIONS ACTIVE: ] {threading.active_count()-1}"
                )
            except Exception as error:
                self.__disconnect_all()
                self.__log_file.write(
                    f"ERROR OCCURED AT:\n {time.ctime()} \n"
                )
                self.__log_file.write(f"> {str(error)}\n")
                self.__log_file.write("================================\n")
                self.__log_file.close()
                exit(1)
