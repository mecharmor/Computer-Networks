import socket
import pickle
import datetime
from TCPClientHandler import TCPClientHandler


class Client:
    def __init__(self, username, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = username
        self.host = host
        self.port = port
        self.tcp_handler = None

    def initial_handshake(self):
        try:
            data = {"msg": "<empty message>",
                    "timestamp": datetime.datetime.now(),
                    "menu_option": 0,
                    "username": self.username
                    }
            data_serialized = pickle.dumps(data)
            self.client.send(data_serialized)
            server_data = pickle.loads(self.client.recv(1024))
            print("Successfully connected to server with IP: " + self.host + " and PORT: " + str(self.port))

            print("Your client info is:")
            print("Client Name: " + self.username)
            print("Client ID: " + str(server_data['client_id']))
        except socket.error as e:
            print("Failed connecting to server with IP: " + self.host + " and PORT: " + str(self.port))
            return

    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            self.initial_handshake()
            self.tcp_handler = TCPClientHandler(self.client, self.username)

            while True:
                menu_selection = self.tcp_handler.next_prompt()
                if menu_selection not in range(1, 7):
                    print("Incorrect option entered. please enter a real menu option")
                    continue
                self.tcp_handler.handle_menu_selection(menu_selection)
                # terminate client if disconnect occurs
                if self.tcp_handler.is_disconnected() is True:
                    break
        except socket.error as socket_exception:
            print(socket_exception)
        self.client.close()


Host_ = 'localhost'  # input("Enter the server IP Address: ")
Port_ = 8008  # input("Enter the server port: ")
Username_ = input("Your id key (i.e your name): ")

# Start Server
client = Client(Username_, Host_, Port_)
client.connect()
