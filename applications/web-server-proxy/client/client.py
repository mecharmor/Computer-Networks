import socket
import pickle
import email
import pprint
from io import StringIO


class Client(object):
    DEBUG = True
    """
    This class represents your client class that will send requests to the proxy server and will hand the responses to 
    the user to be rendered by the browser, 
    """

    def __init__(self):
        self.init_socket()

    def init_socket(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket successfully created")
            if DEBUG:
                print("[client.py -> init_socket] new Client() instantiated")
        except socket.error as err:
            print("socket creation failed with error %s" % err)

    def _connect_to_server(self, host_ip, port):
        try:
            self.client_socket.connect((host_ip, port))
            if DEBUG:
                print("Successfully connected to server")
        except socket.error as err:
            print("socket connection failed with error: %s" % err)
        return 0

    def _send(self, data):
        try:
            serialized = pickle.dumps(data)
            self.client_socket.send(serialized)
            if DEBUG:
                print("[client.py -> _send] sent data to proxy")
        except socket.error as err:
            print("socket send failed with error: %s" % err)
        return 0

    def _receive(self):
        try:
            data = self.client_socket.recv(4096)
            return pickle.loads(data)
            if DEBUG:
                print("[client.py -> _receive] received data from proxy")
        except socket.error as err:
            print("socket recv failed with error %s" % err)

        return {}

    def request_to_proxy(self, data): #[issue], replace sample data
        method = "GET" #or can be POST ??
        http = "1.1"
        host = "127.0.0.1"

        httpRequest = str(method) + """ """ + data['url'] + """ HTTP/""" + http + """\r\n"""
        httpRequest += """Host: """ + str(host) + """\r\n"""
        httpRequest += """Connection: close\r\n"""
        httpRequest += """Keep-Alive: 0\r\n"""
        httpRequest += """is_private_mode: """ + str(data['is_private_mode']) + """\r\n"""
        httpRequest += """\r\n"""

        if DEBUG:
            print("[client.py -> request_to_proxy] sent request to proxy with HTTP format:" + httpRequest)
        
        self._send(httpRequest)

    def response_from_proxy(self):
        response = httpResponseToDictionary(self._receive())
        status_code = response['http_code']
        return response['body']

    def httpResponseToDictionary(response_string):
        # seperate first line and rest
        head, tail = response_string.split("\r\n", 1)
        head = head.split(' ') # head is the top of the response: HTTP/1.1 200 OK\r\n
        response = {}
        response['http'] = head[0].split('/')[-1]
        response['http_code'] = head[1]
        response['headers'] = dict(email.message_from_file(StringIO(tail)).items()) #parse headers and turn into dictionary
        response['body'] = response_string.split("\r\n")[-1] # extract body
        
        if DEBUG:
            print("[client.py -> httpResponseToDictionary] converted to dictionary of:" + response)

        return response

