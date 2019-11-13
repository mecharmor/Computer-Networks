# -*- coding: utf-8 -*-
""" The client
This file has the class client that implements a client socket.
Note that you can replace this client file by your client from
assignment #1.
"""
import socket
import pickle
from logging import Logging

class Client(object):

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logging = Logging()

    def connect(self, host_ip, port):
        try:
            self.client_socket.connect((host_ip, port))
            self.logging.log("client.py -> connect", "connected to host: " + str(host_ip) + ":" + str(port))
        except socket.error as err:
            self.logging.log("client.py -> connect", "failed to connect to host on: " + str(host_ip) + ":" + str(port), 2, str(err))

    def send(self, data):
        try:
            serialized = pickle.dumps(data)
            self.client_socket.send(serialized)
            self.logging.log("client.py -> send", "data sent" + str(data))
        except socket.error as err:
            self.logging.log("client.py -> send", "could not send to socket", 2, str(err))

    def receive(self, memory_allocation_size):
        try:
            serialized_data = self.server.recv(memory_allocation_size)
            deserialized = pickle.loads(serialized_data)
            self.logging.log("client.py -> receive", "received data: " + str(deserialized))
            return deserialized
        except socket.error as err:
            print("socket recv failed with error %s" % err)
            self.logging.log("client.py -> ", "receive", 2, str(err))
        except pickle.UnpicklingError as err:
            self.logging.log("client.py -> receive", "unpickling error!", 2, str(err))

        self.logging.log("client.py -> receive", "an exception occured and receive is returning empty data!!!", 3)
        return {}

    def close(self):
        self.logging.log("client.py -> close", " socket closed!")
        self.client_socket.close()
