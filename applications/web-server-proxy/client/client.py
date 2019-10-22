import socket
import pickle

class Client(object):
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
        except socket.error as err:
            print("socket creation failed with error %s" % err)

    def _connect_to_server(self, host_ip, port):
        try:
            self.client_socket.connect((host_ip, port))
        except socket.error. as err:
            print("socket connection failed with error: %s" % err)
        return 0

    def _send(self, data):
        try:
            serialized = pickle.dumps(data)
            self.client_socket.send(serialized)
        except socket.error as err:
            print("socket send failed with error: %s" % err)
        return 0

    def _receive(self):
        try:
            data = self.client_socket.recv(4096)
            return pickle.loads(data)
        except socket.error as err:
            print("socket recv failed with error %s" % err)

        return {}

    def request_to_proxy(self, data):

        # self._send() this send goes to proxy_server which routes to proxy_thread

        """
        Create the request from data
        request must have headers and can be GET or POST. depending on the option
        then send all the data with _send() method
        :param data: url and private mode 
        :return: VOID
        """
        return 0

    def response_from_proxy(self):
        """
        the response from the proxy after putting the _recieve method to listen.
        handle the response, and then render HTML in browser. 
        This method must be called from web_proxy_server.py which is the home page of the app
        :return: the response from the proxy server
        """
        return 0

