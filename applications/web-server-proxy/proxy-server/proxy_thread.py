"""
Proxy thread file. Implements the proxy thread class and all its functionality. 
"""
import socket
from proxy_manager import ProxyManager
import pickle
import email
import pprint
import datetime
from io import StringIO
import requests # use sparingly
from httpHelper.httpHelper import HttpHelper


class ProxyThread(object):
    MAX_DATA_RECV = 4096
    """
    The proxy thread class represents a threaded proxy instance to handle a specific request from a client socket
    """
    DEBUG = True

    def __init__(self, conn, client_addr, server_ip):
        self.proxy_manager = ProxyManager()
        self.client = conn
        self.client_id = client_addr[1] # get id
        self.client_ip = client_addr[0] #get ip address
        self.server_ip = server_ip

        if self.DEBUG:
            print("[proxy_thread.py -> __init__] new instance of ProxyThread() class ")

    def get_settings(self):
        if self.DEBUG:
            print("[proxy_thread.py -> get_settings] called ")
        return self.proxy_manager

    def init_thread(self):
        while True:
            try:
                data = self._receive() #receiving {'url': url, 'is_private_mode': 0 or 1} from client from web-proxy-server
                self.process_client_request(data)
                if self.DEBUG:
                    print("[proxy_thread.py -> init_thread] data received. data: " + data)
            except socket.error as err:
                print("err")

    def client_id(self):
        if self.DEBUG:
            print("[proxy_thread.py -> client_id] called. returned: " + self.client_id)
        return self.client_id

    def _mask_ip_adress(self):
        self.client_ip = self.server_ip
        if self.DEBUG:
            print("[proxy_thread.py -> _mask_ip_address] set self.client_ip to: " + self.client_ip)

    def process_client_request(self, data):
        p = HttpHelper()
        d = p.convert_http_request_to_dict(data)
        # Main algorithm. Note that those are high level steps, and most of them may
        # require further implementation details
        # 1. get url and private mode status from client 
        url = d['url']
        is_private_mode = d['header']['is_private_mode']
        # 2. if private mode, then mask ip address: mask_ip_address method
        if is_private_mode == 1:
            self._mask_ip_adress()
        # 3. check if the resource (site) is in cache. If so and not private mode, then:
        if self.proxy_manager.is_cached(url) and is_private_mode == 0:
        #     3.1 check if site is blocked for this employee
            if not self.proxy_manager.is_site_blocked(url):
                dontBreak = " "
        #     3.2 check if site require credentials for this employee
                #[issue], legit no clue here
        #     3.3 if 3.1 or 3.2 then then client needs to send a post request to proxy
        #         with credentials to check 3.1 and 3.2 access 
        #         3.3.1 if credentials are valid, send a HEAD request to the original server
        #                 to check last_date_modified parameter. If the cache header for that 
        #                 site is outdated then move to step 4. Otherwise, send a response to the 
        #                 client with the requested site and the appropiate status code.
        # 4. If site is not in cache, or last_data_modified is outdated, then create a GET request 
        if self.proxy_manager.is_cached(url) == False or self.is_outdated_cache(url):
            res = self.response_from_server({'mode': 'GET', 'url': url, 'param': []} )
            #res.headers
            if self.DEBUG:
                print("url: " + url + " status code: " + str(res.status_code))
            print(str(res.headers))
            self.proxy_manager.add_cached_resource(url, res.headers['last-modified'], res.content)

    def is_outdated_cache(self, url):
        list_of_cached = self.proxy_manager.get_cached_resource('cache')
        for item in list_of_cached:
            if item['url'] == url:
                headers = self.response_from_server({'mode': 'HEAD', 'url': url, 'param': []} )
                return headers['last-modified'] == item['last_modified']
        return True

        

    def _send(self, data):
        try:
            serialized = pickle.dumps(data)
            self.client.send(serialized)
            if self.DEBUG:
                print("[proxy_thread.py -> _send] sent data to client: " + data)
        except socket.error as err:
            print("proxy_thread send failed with error %s" % err)
        return

    def _receive(self):
        try:
            serialized = self.client.recv(self.MAX_DATA_RECV)
            data = pickle.loads(serialized)
            if self.DEBUG:
                print("[proxy_thread.py -> _receive] received data from Client: " + data)
            return data
        except socket.error as err:
            print("proxy_thread receive failed with error %s " % err)
        return 0

    def head_request_to_server(self, url, param = ""):
        session = requests.session()
        session.headers['Connection'] = 'close'
        session.headers['Keep-Alive'] = '0'

        try:
            response = session.head(url + param)
            if self.DEBUG:
                print("head_request_to_server: " + response)
            return response.headers # .headers is a dictionary
        except requests.exceptions.MissingSchema:
            #retry logic
            print("request failed. retrying with http:// added to url") 
            response = session.head('http://' + url + param)
            if self.DEBUG:
                print("head_request_to_server: " + response)
            return response.headers # .headers is a dictionary

    def get_request_to_server(self, url, param):
        session = requests.session()
        session.headers['Connection'] = 'close'
        session.headers['Keep-Alive'] = '0'

        try:
            response = session.get(url) #[issue] param list handle elsewhere
            if self.DEBUG:
                print("get_request_to_server: " + str(response))
            return response # .headers, .content, .json, .status_code
        except requests.exceptions.MissingSchema:
            #retry logic
            print("request failed. retrying with http:// added to url") 
            response = session.get('http://' + url) #[issue], param list handle somehow
            if self.DEBUG:
                print("get_request_to_server: " + str(response))
            return response

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

        #[issue, NEED TO SEND DATA TO CLIENT. RIGHT NOW DATA IS SAVED BUT NOT USED
        #[issue], parse data here
        
        #converted = self.create_response_for_client("1.1", "REPLACE_ME", "<! DOCTYPE html>", 200)
        self._send(converted)

    # def create_response_for_client(self,http_version, last_modified, html, status_code = 200):

    #     # #[issue] default for testing
    #     # last_modified = "Tue, 30 Oct 2007 17:00:02"
    #     # date = datetime.datetime.now()
    #     # status_code = 200

    #     # response = """HTTP/""" + str(http_version) + " " + str(status_code) + """\r\n"""
    #     # response += """Date: """ + str(date) + """\r\n"""
    #     # response += """Last-Modified: """ + str(last_modified) + """\r\n"""
    #     # if str(http_version) == "1.1":
    #     #     response += """Connection: close\r\n"""
    #     #     response += """Keep-Alive: 0\r\n"""
    #     # response += """\r\n"""
    #     # response += html #attach html


    #     if self.DEBUG:
    #         print("[proxy_thread.py -> create_response_for_client] response constructed: " + response)

    #     return response


   





# print("Unit Test for Proxy_thread")
#
# pt = ProxyThread()
# print(pt.get_request_to_server("http://www.google.com", "Connection: close"))






# REFERENCE MATERIAL

# format of response string
# HTTP/1.1 200 OK\r\n
# Date: Sun, 26 Sep 2010 20:09:20 GMT\r\n
# Server: Apache/2.0.52 (CentOS)\r\n
# Last-Modified: Tue, 30 Oct 2007 17:00:02 GMT\r\n
# ETag: "17dc6-a5c-bf716880"\r\n
# Accept-Ranges: bytes\r\n
# Content-Length: 2652\r\n
# Keep-Alive: timeout=10, max=100\r\n
# Connection: Keep-Alive\r\n
# Content-Type: text/html; charset=ISO-8859-1\r\n
# \r\n
# data data data data data ...

# garbage
        # url = data['url']
        # is_private_mode = data['is_private_mode']

        # if is_private_mode == True or is_private_mode == 1:
        #     self._mask_ip_adress()
            
        # if self.proxy_manager.is_cached(url) and not is_private_mode:
        #     #do 3.1
        #     if not self.proxy_manager.is_site_blocked(url):
        #     # 3.2 check if site require credentials for this employee
        #         #self.send_response_to_client() POST request
        #         response = self.response_from_server({'mode': 'HEAD', 'url': url, 'param': []})
        #         response_dict = self.httpResponseToDictionary(response)
        #         cached_resource = self.proxy_manager.get_cached_resource(url) # get resource
        #         #get last modified date and compare with cached_resource['Last-Modified'] == response['header']['Last-Modified']
        #         if True: # if cache and response dates are same
        #             self.send_response_to_client()

        # elif 