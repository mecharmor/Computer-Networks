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

    def __init__(self, ip, port):
        self.logging = Logging()
        self.host = ip
        self.port = port
        self.max_connections = 20
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

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
                threading._start_new_thread(self.handle_connection, (conn, addr))
                self.logging.log("server.py -> accept", "new client joined: " + str(addr[1]))
        except socket.error as err:
            print("accept new client failed with error %s" % str(err))
            self.logging.log("server.py -> accept", "accept new client failed", 2, str(err))

    def receive(self, socket_conn, memory_allocation_size):
        try:
            serialized_data = socket_conn.recv(memory_allocation_size)
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

    def send(self, socket_conn, data):
        try:
            serialized = pickle.dumps(data)
            socket_conn.send(serialized)
            self.logging.log("server.py -> send", "data sent" + str(data))
        except socket.error as err:
            self.logging.log("server.py -> send", "could not send to socket", 2, str(err))

    def handle_connection(self, conn, addr):
        self.logging.log("server.py -> handle_connection", "client connected: " + str(addr[0]))
        self.clients.append((conn, addr))
        # I am confused what to do here
        # data = self.receive(conn, 100000)

    def get_connected_clients_list(self):
        return self.clients
