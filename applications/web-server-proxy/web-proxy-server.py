from flask import Flask
from flask import Flask, render_template, request, redirect
import requests
import client

app = Flask(__name__)


@app.route('/')
def home():

    # [note], need to find flask function to render page with http response
    # return      """
    #             GET /index.html HTTP/1.1\r\n
    #     Host: www-net.cs.umass.edu\r\n
    #     User-Agent: Firefox/3.6.10\r\n
    #     Connection: close\r\n
    #     Accept: text/html,application/xhtml+xml\r\n
    #     Accept-Language: en-us,en;q=0.5\r\n
    #     Accept-Encoding: gzip,deflate\r\n
    #     Accept-Charset: ISO-8859-1,utf-8;q=0.7\r\n
    #     Keep-Alive: 115\r\n
    #     Connection: keep-alive\r\n
    #     \r\n
    #     <html><head><title>yooo</title></head><body><h1>yoooooo</h1></body></html>
    #     """
    return render_template('home.html')


@app.route('/proxy-settings')
def proxy_settings():
    return render_template('proxy-settings.html')


@app.route('/home.html', methods=['POST'])
def get_user_input():
    url = request.form.get('url')
    is_private_mode = 0
    if request.form.get('private'):
        is_private_mode = 1
    if "proxy-settings" in url:
        return proxy_settings()
    data = {'url': url, 'is_private_mode': is_private_mode}
    client = Client()
    client.request_to_proxy(data)
    
    # client = Client(data)
    # client.run()
    # client.send_request()
    # client.get_respones()

    return client.response_from_proxy()


if __name__ == '__main__':
    app.run()
