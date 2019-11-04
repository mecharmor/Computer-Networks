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
import os
import requests  # use sparingly
from httpHelper.httpHelper import HttpHelper


class ProxyThread(object):
    MAX_DATA_RECV = 1000000000
    """
    The proxy thread class represents a threaded proxy instance to handle a specific request from a client socket
    """
    DEBUG = False

    def __init__(self, conn, client_addr):
        self.proxy_manager = ProxyManager()
        self.client = conn
        self.client_id = client_addr[1]  # get id
        self.client_ip = client_addr[0]  # get ip address
        self.http_version = "1.1"

        if self.DEBUG:
            print("[proxy_thread.py -> __init__] new instance of ProxyThread() class ")

    def get_settings(self):
        if self.DEBUG:
            print("[proxy_thread.py -> get_settings] called ")
        return self.proxy_manager

    def init_thread(self):
        try:
            data = self._receive()
            self.process_client_request(data)
            if self.DEBUG:
                print("[proxy_thread.py -> init_thread] data received. data: \n" + str(data))
        except socket.error as err:
            print("[proxy_thread -> init_thread] error! " + str(err))

    def client_id(self):
        if self.DEBUG:
            print("[proxy_thread.py -> client_id] called. returned: " +
                  str(self.client_id))
        return self.client_id

    def _mask_ip_adress(self):
        # the proxy server is already masking the user IP
        if self.DEBUG:
            print(
                "[proxy_thread.py -> _mask_ip_address] set self.client_ip to: " + str(self.client_ip))

    def process_client_request(self, data):
        req = HttpHelper().convert_http_request_to_dict(data)
        self.http_version = req['http']
        url = req['url']
        is_private_mode = req['header']['is_private_mode']

        username = req['header']['username'] # fetch username
        password = req['header']['password'] # fetch password

        # if private mode then mask ip
        if is_private_mode == 1:
            self._mask_ip_adress()

        if self.proxy_manager.is_site_blocked(url):
            if self.proxy_manager.is_admin(username, password):
                self.check_cache_and_send_to_client(url)
            else:
                self.send_response_to_client(str(407), "",
                """<!DOCTYPE html>
                <html>
                    <head>
                        <title>407 Proxy Authentication Required</title>
                    </head>
                    <body>
                        <h1>407 Proxy Authentication Required</h1><p> the proxy needs authorization based on client credentials in order to continue with the request. (try logging in as admin)</p>
                    </body>
                </html>""")
            
        elif self.proxy_manager.is_site_blocked_except_managers(url):
            if self.proxy_manager.is_manager(username, password) or self.proxy_manager.is_admin(username, password):
                self.check_cache_and_send_to_client(url)
            else:
                self.send_response_to_client(str(401), "",
                """<!DOCTYPE html>
                    <html>
                        <head>
                            <title>401</title>
                        </head>
                        <body>
                            <h1>401 Unauthoritzed</h1><p> resource is blocked or not authorized for the current user</p>
                        </body>
                    </html>""")
        else:
            self.check_cache_and_send_to_client(url)

    def check_cache_and_send_to_client(self, url):
        if self.proxy_manager.is_cached(url) and not self.is_outdated_cache(url): # <-- crashing here
            cached_site = self.proxy_manager.get_cached_resource(url)  # contains url, last_modified, and html
            self.send_response_to_client(str(200), cached_site['last_modified'], cached_site['html']) # response

        else: # website not cached or might be outdated resource
            res = self.response_from_server({'mode': 'GET', 'url': url, 'param': []})
            if self.DEBUG:
                print("url: " + url + " status code: " + str(res.status_code))
                print("headers: " + str(res.headers))

            # add to cache
            try:
                self.proxy_manager.add_cached_resource(url, res.headers['last-modified'], str(res.content))
            except KeyError as e:
                print("proxy_thread, last-modified header did not exist: " + str(e))
                self.proxy_manager.add_cached_resource(url, res.headers['date'], str(res.content))

            # send response
            last_modified = ""
            try:
                last_modified = res.headers['last-modified']
            except KeyError:
                last_modified = res.headers['date']
            self.send_response_to_client(res.status_code, last_modified, str(res.content))

    def is_outdated_cache(self, url):
        cache = self.proxy_manager.get_cached_resource(url)
        headers = self.response_from_server({'mode': 'HEAD', 'url': str(url), 'param': []})
        try:
            return headers['last-modified'] == cache['last_modified']
        except KeyError as err:
            print("outdated cache: " + str(err))
        return False #returning false to fake success in cache

    def _send(self, data):
        try:
            serialized = pickle.dumps(data)
            self.client.send(serialized)
            if self.DEBUG:
                print("[proxy_thread.py -> _send] sent data to client: " + str(data))
        except socket.error as err:
            print("proxy_thread send failed with error %s" % err)
        return

    def _receive(self):
        while True:
            try:
                serialized = self.client.recv(self.MAX_DATA_RECV)
                data = pickle.loads(serialized)
                if self.DEBUG:
                    print(
                        "[proxy_thread.py -> _receive] received data from Client: \n" + str(data))
                return data
            except socket.error as err:
                print("proxy_thread receive failed with error %s " % err)
            except EOFError:
                # print("[proxy_thread -> _receive] EOFError! (unable to pickle.loads successfully)")
                print("proxy thread EOFError exiting...")
                return "     "
                pass

    def head_request_to_server(self, url):
        session = requests.session()
        session.headers['Connection'] = 'close'
        session.headers['Keep-Alive'] = '0'

        try:
            response = session.head(url)
            if self.DEBUG:
                print("head_request_to_server: " + response)
            return response.headers  # .headers is a dictionary
        except requests.exceptions.MissingSchema:
            # retry logic
            print("request failed. retrying with http:// added to url")
            response = session.head('http://' + url )
            if self.DEBUG:
                print("head_request_to_server: " + response)
            return response.headers  # .headers is a dictionary

    def get_request_to_server(self, url):
        session = requests.session()
        session.headers['Connection'] = 'close'
        session.headers['Keep-Alive'] = '0'

        try:
            response = session.get(url)
            if self.DEBUG:
                print("get_request_to_server: " + str(response))
            return response  # .headers, .content, .json, .status_code
        except requests.exceptions.MissingSchema:
            # retry logic
            print("request failed. retrying with http:// added to url: " + "http://" + url)
            response = session.get('http://' + url)
            if self.DEBUG:
                print("get_request_to_server: " + str(response))
            return response

    def response_from_server(self, request):
        mode = request['mode']
        url = request['url']
        if mode == "GET":
            return self.get_request_to_server(url)
        return self.head_request_to_server(url)

    def send_response_to_client(self, status_code, last_modified, html):
        response_string = HttpHelper().build_http_response(
            self.http_version, str(status_code), last_modified, str(html))
        self._send(response_string)