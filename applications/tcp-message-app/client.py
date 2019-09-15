import socket
import pickle
import datetime


class Client:
    def __init__(self, username, host, port):
        self.client = None
        self.username = username
        self.host = host
        self.port = port

    def send_message(self, client_route, msg="<NO MESSAGE>"):
        data = {"msg": msg,
                "timestamp": datetime.datetime.now(),
                "client_route": client_route,
                "username": self.username
                }
        data_serialized = pickle.dumps(data)
        self.client.send(data_serialized)

    def receive_message(self):
        # THIS NEEDS TO USE THE TCPClientHandler class

        server_response = self.client.recv(1024)
        # Deserialize the data.
        server_data = pickle.loads(server_response)
        # Get all the values in the data dictionary
        client_id = server_data['client_id']  # the client id assigned by the server
        server_msg = server_data['msg']
        print("Client " + str(client_id) + " successfully connected to server")
        print("Server says: " + server_msg)

    def initial_handshake(self):
        self.send_message(0)  # 0 selection is the initial handshake with server

        server_data = None
        try:
            server_data = pickle.loads(self.client.recv(1024))
            print("Successfully connected to server with IP: " + self.host + " and PORT: " + str(self.port))
        except socket.error as e:
            print("Failed connecting to server with IP: " + self.host + " and PORT: " + str(self.port))
            return

        print("Your client info is:")
        print("Client Name: " + self.username)
        print("Client ID: " + str(server_data['client_id']))

    def connect(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connects to the server using its host IP and port
            self.client.connect((self.host, self.port))
            self.initial_handshake()

            while True:
                self.send_message(3, input("Enter Message: "))
                self.receive_message()

        except socket.error as socket_exception:
            print(socket_exception)  # An exception occurred at this point
        self.client.close()


Host_ = 'localhost'  # input("Enter the server IP Address: ")
Port_ = 8008  # input("Enter the server port: ")
Username_ = input("Your id key (i.e your name): ")

# Start Server
client = Client(Username_, Host_, Port_)
client.connect()
