import socket
import pickle
import datetime
import TCPClientHandler

# Globals
Host = input("Enter the server IP Address: ")
Port = int(input("Enter the server port:"))
ClientName = input("Your id key (i.e your name):")


def ConnectToServer():
    client.connect((Host, Port))


def Send(_data):
    # Serialization
    data_serialized = pickle.dumps(_data)
    client.send(data_serialized)


def Receive():
    # TCPClientHandler handles response
    # Server Response
    server_response = client.recv(1024)
    # Desearialize data
    server_data = pickle.loads(server_response)
    return server_data


# Create Socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Sample Json Data
data = {"msg_from_client": "Hello from client!",
        "sent_on": datetime.datetime.now()}

ConnectToServer()
Send(data)
# Get values in dictionary
# client_id = data['client_id']
# server_msg = data['msg_from_server']

client.close()
