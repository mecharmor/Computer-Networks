import os
import sys
import threading
import socket
from proxy_thread import ProxyThread


class ProxyServer(object):
    HOST = '127.0.0.1'
    PORT = 9000
    #BACKLOG = 50
    MAX_DATA_RECV = 1000000000  # 4096

    def __init__(self):
        self.clients = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        print("IP Address: " + self.HOST)
        print("Listening on port " + str(self.PORT) + " ...")
        print("Waiting for connections...")
        threading._start_new_thread(self.wait_for_termination, ())
        try:
            self.server.bind((self.HOST, self.PORT))
            self.server.listen(20)
            self.accept_clients()
        except socket.error as e:
            print("server failed: " + str(e))

    def wait_for_termination(self):
        # use this for server shutdown
        while True:
            user_input = input("enter 'quit' to terminate server safely -->")
            if user_input == 'quit':
                for client_sock, addr in self.clients:
                    print("client closed forcefully: " + str(addr[1]))
                    client_sock.close()
                self.server.close()
                break

    def accept_clients(self):
        try:
            while True:
                # Note: addr[0] is client IP, addr[1] is socket id
                client_sock, addr = self.server.accept()
                # record connected client
                self.clients.append((client_sock, addr))
                threading._start_new_thread(self.proxy_thread, (client_sock, addr))
                print("[proxy_server -> accept_clients] new client joined: " + str(addr[1]))
        except socket.error as err:
            print("accept new client failed with error %s" % err)

    def proxy_thread(self, conn, client_addr):
        proxy_thread = ProxyThread(conn, client_addr)
        proxy_thread.init_thread()


server = ProxyServer()
server.run()
