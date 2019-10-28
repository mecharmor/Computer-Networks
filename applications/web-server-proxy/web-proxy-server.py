from flask import Flask
from flask import Flask, render_template, request, redirect
import requests
from client.client import Client

# from proxy_manager import ProxyManager

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/proxy-settings")
def proxy_settings():
    # pm = ProxyManager()
    print("success")
    return render_template("proxy-settings.html")


@app.route("/home.html", methods=["POST"])
def get_user_input():
    url = request.form.get("url")
    is_private_mode = 0
    if request.form.get("private"):
        is_private_mode = 1
    if "proxy-settings" in url:
        return proxy_settings()
    data = {"url": url, "is_private_mode": is_private_mode}
    client = Client()
    client.request_to_proxy(data)

    return client.response_from_proxy()


# @app.route('/proxy-settings', methods=['POST'])
# def get_user_input():
#     print("ok")


#     return "hi"


if __name__ == "__main__":
    app.run()


# reference
# client = Client(data)
# client.run()
# client.send_request()
# client.get_respones()