import socket
import pickle
import datetime

# Steps
# 1) connect to server
#     - prompt for host and port
#     - server responds with client id
# output connected. if fail then close client
# 2) send requests to the server
# get list of users from server
# output list to console
# 3) retrieve responses from the server
# 3.5) responses are handled by the class TCPClientHandler
# TCPClientHandler --> handles all the menu actions executed from the client side

# Client class will have methods: client.open() client.close()
