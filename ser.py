import socket
import threading
import time


class Ser:
    __log_file = open("log.txt", 'a')
    __connected_list = []
    _host_name = None
    _host_ip = socket.gethostbyname(socket.gethostname())
    diss_msg = "!DISSCONNECT"
    _header = 64
    _port = 5050
    _frmt = 'utf-8'
    _addr = None

    def __init__(self, host):
        self._host_name = host
        self._addr = (self._host_ip, self._port)

    def __disconnect_all(self):
        for _ in self.__connected_list:
            _.close()

    def handler(self, conn, addr):
        print(f"[NEW CON] {addr} connected")
        conned = True
        while conned:
            msg_len = len(conn.recv(self._header).decode(self._frmt))
            if msg_len:
                msg_len = int(msg_len)
                msg = conn.recv(msg_len).decode(self._frmt)
                if msg == self.diss_msg:
                    conned = False
                    self.__connected_list.pop(
                        self.__connected_list.index(conn))
                print(f"{addr} - {msg}")
        conn.close()

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self._addr)
        print("[STARTING]")
        self.server.listen()
        print(f"Server is listening on {self.server}")
        while True:
            try:
                conn, self._addr = self.server.accept()
                try:
                    thr = threading.Thread(
                        target=self.handler, args=(conn, self._addr)
                    )
                    self.__connected_list += conn
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
            except KeyboardInterrupt:
                print("Closing server")
                self.__disconnect_all()
                exit(0)
