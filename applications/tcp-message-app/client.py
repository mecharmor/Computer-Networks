# ------------- Steps To Follow -------------------
# 1) connect to server
#  - prompt for host and port
#  - server responds with client id
# output connected. if fail then close client
# 2) send requests to the server
# get list of users from server
# output list to console
# 3) retrieve responses from the server
# 3.5) responses are handled by the class TCPClientHandler
# TCPClientHandler --> handles all the menu actions executed from the client side

import socket
import pickle
import datetime

# start
Host = input("Enter the server IP Address: ")
Port = input("Enter the server port:")

# Create Socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client.connect((Host, Port))

# Serialization
data = {"msg_from_client": "Hello from client!",
        "sent_on": datetime.datetime.now()}
data_serialized = pickle.dumps(data)
client.send(data_serialized)

# Server Response
server_response = client.recv(1024)
# Desearialize data
server_data = pickle.loads(server_response)
# Get values in dictionary
#client_id = data['client_id']
#server_msg = data['msg_from_server']

client.close()
