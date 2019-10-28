import email
from io import StringIO
class HttpHelper:

    def __init__(self):
        self.DEBUG = True

    def convert_http_response_to_dict(self, response_string):
        # seperate first line and rest
        head, tail = response_string.split("\r\n", 1)
        head = head.split(' ') # head is the top of the response: HTTP/1.1 200 OK\r\n
        response = {}
        response['http'] = head[0].split('/')[-1]
        response['http_code'] = head[1]
        response['headers'] = dict(email.message_from_file(StringIO(tail)).items()) #parse headers and turn into dictionary
        response['body'] = response_string.split("\r\n")[-1] # extract body

        if self.DEBUG:
            print("[httpHelper.py -> ] converted to dictionary: " + response)

        return response
        
    def convert_http_request_to_dict(self, request_string):
        # seperate first line and headers + body
        top, headers = request_string.split("\r\n", 1)
        top = top.split(' ') # Top is the top of the reseponse: GET www.google.com HTTP/1.1
        request = {}
        request['method'] = top[0]
        request['url'] = top[1]
        request['http'] = top[2].split('/')[-1]
        request['header'] = dict(email.message_from_file(StringIO(headers)).items()) #parse headers and turn into dictionary
        request['body'] = request_string.split("\r\n")[-1] # extract body

        if self.DEBUG:
            print("[proxy_thread.py -> httpRequestToDictionary] dictionary created: " + str(request))

        return request

    def build_http_request(self, url, host, is_private_mode, method = "GET", http = "1.1"):
        httpRequest = str(method) + """ """ + str(url) + """ HTTP/""" + http + """\r\n"""
        httpRequest += """Host: """ + str(host) + """\r\n"""
        httpRequest += """Connection: close\r\n"""
        httpRequest += """Keep-Alive: 0\r\n"""
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





