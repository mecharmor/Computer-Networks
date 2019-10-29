import os, sys, threading, socket
from proxy_thread import ProxyThread


class ProxyServer(object):
    HOST = '127.0.0.1'
    PORT = 9000
    #BACKLOG = 50
    MAX_DATA_RECV = 1000000000 #4096

    def __init__(self):
        self.clients = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        print("IP Address: " + self.HOST)
        print("Listening on port " + str(self.PORT) + " ...")
        print("Waiting for connections...")
        try:
            self.server.bind((self.HOST, self.PORT))
            self.server.listen(20)
            self.accept_clients()
        except socket.error as e:
            print("server failed: " + str(e))

    def accept_clients(self):
        try:
            while True:
                client_sock, addr = self.server.accept()  # Note: addr[0] is client IP, addr[1] is socket id
                self.clients.append((client_sock, addr))  # record connected client
                threading.Thread(target=self.proxy_thread, args=(client_sock, addr, self.HOST)).start()
        except socket.error as err:
            print("accept new client failed with error %s" % err)

    def proxy_thread(self, conn, client_addr, host):
        proxy_thread = ProxyThread(conn, client_addr, host)
        proxy_thread.init_thread()


server = ProxyServer()
server.run()
