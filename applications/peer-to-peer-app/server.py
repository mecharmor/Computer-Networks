# -*- coding: utf-8 -*-
""" The server
This file has the class client that implements a server socket.
Note that you can replace this server file by your server from
assignment #1.
"""
import socket
import pickle
import threading
from logging import Logging

class Server(object):

    def __init__(self):
        self.logging = Logging()
        self.host = '127.0.0.1'
        self.port = 12000
        self.max_connections = 20
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def listen(self):
        print("Listening On " + self.host + ":" + str(self.port))
        print("Waiting For Connections...")
        self.logging.log("server.py -> listen", "Listening On " + self.host + ":" + str(self.port))
        threading._start_new_thread(self.wait_for_termination, ())
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(self.max_connections)
            self.accept()
        except socket.error as e:
            print("server failed with error: " + str(e))
            self.logging.log("server.py -> listen", "server failed with error: ", 2, str(e))

    def wait_for_termination(self):
        # forced server shutdown
        while True:
            user_input = input("enter 'quit' to terminate server safely...\n")
            if user_input == 'quit':
                self.logging.log("server.py -> wait_for_termination", "server terminated by user")
                self.server.close() # close server
                break

    def accept(self):
        try:
            while True:
                conn, addr = self.server.accept() # Note: addr[0] is client IP, addr[1] is socket id
                threading._start_new_thread(self.threaded_client, (conn, addr))
                self.logging.log("server.py -> accept", "new client joined: " + str(addr[1]))
        except socket.error as err:
            print("accept new client failed with error %s" % str(err))
            self.logging.log("server.py -> accept", "accept new client failed", 2, str(err))

    def receive(self, memory_allocation_size):
        try:
            serialized_data = self.server.recv(memory_allocation_size)
            deserialized = pickle.loads(serialized_data)
            self.logging.log("server.py -> receive", "received data: " + str(deserialized))
            return deserialized
        except socket.error as err:
            print("socket recv failed with error %s" % err)
            self.logging.log("server.py -> ", "receive", 2, str(err))
        except pickle.UnpicklingError as err:
            self.logging.log("server.py -> receive", "unpickling error!", 2, str(err))

        self.logging.log("server.py -> receive", "an exception occured and receive is returning empty data!!!", 3)
        return None

    def send(self, data):
        try:
            serialized = pickle.dumps(data)
            self.server.send(serialized)
            self.logging.log("server.py -> send", "data sent" + str(data))
        except socket.error as err:
            self.logging.log("server.py -> send", "could not send to socket", 2, str(err))

    def threaded_client(self, conn, client_addr):
        self.logging.log("server.py -> threaded_client", "threaded client running")
        """
        TODO: implement this method
        :param conn:
        :param client_addr:
        :return: a threaded client.
        """
        # [issue], implement here!! 
        # create a Client here
        return None
