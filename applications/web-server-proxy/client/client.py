import socket
import pickle
import email
from io import StringIO

class HttpHelper:

    def __init__(self):
        self.DEBUG = False

    def convert_http_response_to_dict(self, response_string):
        # seperate first line and rest
        head, tail = response_string.split("\r\n", 1)
        head = head.split(' ') # head is the top of the response: HTTP/1.1 200 OK\r\n
        response = {}
        response['http'] = head[0].split('/')[1]
        response['http_code'] = head[1]
        response['headers'] = dict(email.message_from_file(StringIO(tail)).items()) #parse headers and turn into dictionary
        response['body'] = response_string.split("\r\n")[-1] # extract body

        if self.DEBUG:
            print("[httpHelper.py -> ] converted to dictionary: " + str(response))

        return response

    def convert_http_request_to_dict(self, request_string):
        # seperate first line and headers + body
        top, headers = request_string.split("\r\n", 1)
        new_top = top.split(' ') # Top is the top of the reseponse: GET www.google.com HTTP/1.1
        request = {}
        request['method'] = new_top[0]
        request['url'] = new_top[1]
        request['http'] = top.split('/')[-1]
        request['header'] = dict(email.message_from_file(StringIO(headers)).items()) #parse headers and turn into dictionary
        request['body'] = request_string.split("\r\n")[-1] # extract body

        if self.DEBUG:
            print("[proxy_thread.py -> httpRequestToDictionary] dictionary created: " + str(request))

        return request

    def build_http_request(self, url, host, is_private_mode, method = "GET", http = "1.1", username = "", password = ""):
        httpRequest = str(method) + """ """ + str(url) + """ HTTP/""" + http + """\r\n"""
        httpRequest += """Host: """ + str(host) + """\r\n"""
        httpRequest += """Connection: close\r\n"""
        httpRequest += """Keep-Alive: 0\r\n"""
        httpRequest += """username:""" + username + """\r\n"""
        httpRequest += """password:""" + password + """\r\n"""
        httpRequest += """is_private_mode: """ + str(is_private_mode) + """\r\n"""
        httpRequest += """\r\n"""

        return httpRequest

    def build_http_response(self,http_version, status_code, last_modified, html):
        response = """HTTP/""" + str(http_version) + " " + str(status_code) + """\r\n"""
        # response += """Date: """ + str(date) + """\r\n"""
        response += """Last-Modified: """ + str(last_modified) + """\r\n"""
        if str(http_version) == "1.1":
            response += """Connection: close\r\n"""
            response += """Keep-Alive: 0\r\n"""
        response += """\r\n"""
        response += html #attach html

        return response


class Client(object):
    DEBUG = True
    """
    This class represents your client class that will send requests to the proxy server and will hand the responses to 
    the user to be rendered by the browser, 
    """

    def __init__(self):
        self.MAX_RECV = 1000000000
        self.my_ip = "10.0.0.5"
        self.http_version = "1.1" # "1.0" to test later
        self.httpHelper = HttpHelper()
        self.init_socket()

    def init_socket(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._connect_to_server('127.0.0.1', 9000)
            print("Socket successfully created")
            if self.DEBUG:
                print("[client.py -> init_socket] new Client() instantiated")
        except socket.error as err:
            print("socket creation failed with error %s" % err)

    def _connect_to_server(self, host_ip, port):
        try:
            self.client_socket.connect((host_ip, port))
            if self.DEBUG:
                print("Successfully connected to server")
        except socket.error as err:
            print("socket connection failed with error: %s" % err)
        return 0

    def _send(self, data):
        try:
            serialized = pickle.dumps(data)
            self.client_socket.send(serialized)
            if self.DEBUG:
                print("[client.py -> _send] sent data to proxy")
        except socket.error as err:
            print("socket send failed with error: %s" % err)
        return 0

    def _receive(self):
        try:
            data = self.client_socket.recv(self.MAX_RECV)
            return pickle.loads(data)
            if self.DEBUG:
                print("[client.py -> _receive] received data from proxy")
        except socket.error as err:
            print("socket recv failed with error %s" % err)
        except pickle.UnpicklingError:
            print("website is too large for data. (delete database and try again)")

        return {}

    def request_to_proxy(self, data):
        # given {'url': url, 'is_private_mode': is_private_mode}
        
        # build request
        request = self.httpHelper.build_http_request(
                                                     data['url'], 
                                                     self.my_ip, 
                                                     data['is_private_mode'], 
                                                     "GET", 
                                                     self.http_version,
                                                     data['username'],
                                                     data['password'])

        if self.DEBUG:
            print("[client.py -> request_to_proxy] sent request to proxy with HTTP format:\n" + str(request))
        
        self._send(request)

    def response_from_proxy(self):
        response_string = self._receive()

        response = self.httpHelper.convert_http_response_to_dict(response_string)
        #[issue], handle more response codes here
        # the value returned from this function will be rendered on client screen
        status_code = response['http_code']
        if status_code == 200:
            print("SUCCESS response from proxy")
        elif status_code == 500:
            print("internal server error happened here")

        return response['body']


