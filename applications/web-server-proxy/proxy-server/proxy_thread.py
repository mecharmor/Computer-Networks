"""
Proxy thread file. Implements the proxy thread class and all its functionality. 
"""
import socket
from proxy_manager import ProxyManager
import pickle
# IMPORTANT READ BELOW NOTES. Otherwise, it may affect negatively your grade in this assignment
# Note about requests library
# use this library only to make request to the original server inside the appropriate class methods
# you need to create your own responses when sending them to the client (headers and body)
# request from client to the proxy are just based on url and private mode status. client also
# will send post requests if the proxy server requires authentication for some sites.
import requests


class ProxyThread(object):
    MAX_DATA_RECV = 4096
    """
    The proxy thread class represents a threaded proxy instance to handle a specific request from a client socket
    """

    def __init__(self, conn, client_addr):
        self.proxy_manager = ProxyManager()
        self.client = conn
        self.client_id = client_addr[1]

    def get_settings(self):
        return self.proxy_manager

    def init_thread(self):
        while True:
            try:
                data = self.client.recv(self.MAX_DATA_RECV)
                deserialized = pickle.loads(data)
                self.process_client_request(deserialized)

    def client_id(self):
        return self.client_id

    def _mask_ip_adress(self):
        """
        When private mode, mask ip address to browse in private
        This is easy if you think in terms of client-server sockets
        :return: VOID
        """
        return 0

    def process_client_request(self, data):
        url = data['url']
        is_private_mode = data['is_private_mode']

        if is_private_mode :
            self._mask_ip_adress()
        if self.proxy_manager.is_cached(data) and is_private_mode == 0: #3
            #3.1
        else: #what happens when we are in private mode?
            self.get_request_to_server(self, url, )



        """
       Main algorithm. Note that those are high level steps, and most of them may
       require further implementation details
       1. get url and private mode status from client 
       2. if private mode, then mask ip address: mask_ip_address method
       3. check if the resource (site) is in cache. If so and not private mode, then:
           3.1 check if site is blocked for this employee 
           3.2 check if site require credentials for this employee
           3.3 if 3.1 or 3.2 then then client needs to send a post request to proxy
               with credentials to check 3.1 and 3.2 access 
               3.3.1 if credentials are valid, send a HEAD request to the original server
                     to check last_date_modified parameter. If the cache header for that 
                     site is outdated then move to step 4. Otherwise, send a response to the 
                     client with the requested site and the appropiate status code.
        4. If site is not in cache, or last_data_modified is outdated, then create a GET request 
           to the original server, and store in cache the response from the server. 
       :param data: 
       :return: VOID
       """
        return 0

    def _send(self, data):
        try:
            serialized = pickle.dumps(data)
            self.client.send(serialized)
        except socket.error as err:
            print("proxy_thread send failed with error %s" % err)
        return

    def _receive(self):
        try:
            data = self.client.recv(self.MAX_DATA_RECV)
            return pickle.loads(data)
        except socket.error as err:
            print("proxy_thread receive failed with error %s " % err)
        return 0

    def head_request_to_server(self, url, param):
        return requests.head(url + param).headers
        """
        HEAD request does not return the HTML of the site
        :param url:
        :param param: parameters to be appended to the url
        :return: the headers of the response from the original server
        """

    def get_request_to_server(self, url, param):
        return requests.get(url, param)

    def response_from_server(self, request):
        """
        Method already made for you. No need to modify
        :param request: a python dictionary with the following 
                        keys and values {'mode': 'GET OR HEAD', 'url': 'yoursite.com', 'param': []} 
        :return: 
        """
        mode = request['mode']
        url = request['url']
        param = request['param']
        if mode == "GET":
            return self.get_request_to_server(url, param)
        return self.head_request_to_server(url, param)

    def send_response_to_client(self, data):
        """
                GET /index.html HTTP/1.1\r\n
        Host: www-net.cs.umass.edu\r\n
        User-Agent: Firefox/3.6.10\r\n
        Connection: close\r\n
        Accept: text/html,application/xhtml+xml\r\n
        Accept-Language: en-us,en;q=0.5\r\n
        Accept-Encoding: gzip,deflate\r\n
        Accept-Charset: ISO-8859-1,utf-8;q=0.7\r\n
        Keep-Alive: 115\r\n
        Connection: keep-alive\r\n
        \r\n

        The response sent to the client must contain at least the headers and body of the response 
        :param data: a response created by the proxy. Please check slides for response format
        :return: VOID
        """
        return 0

    def create_response_for_client(self):
        """
        
        :return: the response that will be passed as a parameter to the method send_response_to_client()
        """
        return 0


# print("Unit Test for Proxy_thread")
#
# pt = ProxyThread()
# print(pt.get_request_to_server("http://www.google.com", "Connection: close"))