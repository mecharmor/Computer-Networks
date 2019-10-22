import os, sys, threading, socket
from proxy_thread import ProxyThread


class ProxyServer(object):
    HOST = '127.0.0.1'
    PORT = 12000
    BACKLOG = 50
    MAX_DATA_RECV = 4096

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
        except socket.error as (value, message):
            print(message)

    def accept_clients(self):
        try:
            while True:
                client_sock, addr = self.server.accept()  # Note: addr[0] is client IP, addr[1] is socket id
                self.clients.append((client_sock, addr))  # record connected client
                threading.Thread(target=self.proxy_thread, args=(client_sock, addr)).start()
        except socket.error as err:
            print("accept new client failed with error %s" % err)
        return 0

    def proxy_thread(self, conn, client_addr):
        """
        I made this method for you. It is already completed and no need to modify it. 
        This already creates the threads for the proxy is up to you to find out where to put it.
        Hint: since we are using only  non-persistent connections. Then, when a clients connects, 
        it also means that it already has a request to be made. Think about the difference 
        between this and assign#1 when you created a new thread. 
        :param conn: 
        :param client_addr: 
        :return: 
        """
        proxy_thread = ProxyThread(conn, client_addr)
        proxy_thread.init_thread()


server = ProxyServer()
server.run()
