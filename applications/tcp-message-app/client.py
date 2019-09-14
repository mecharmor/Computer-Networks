import socket
import pickle
import datetime

HOST = 'localhost'  # The server IP address. Use localhost for this project
PORT = 8008  # The server port


def SendMessage(menu_selection, msg="Hello from Client (test)!"):
    data = {"msg": msg,
            "timestamp": datetime.datetime.now(),
            "menu_selection": menu_selection
            }
    data_serialized = pickle.dumps(data)
    client.send(data_serialized)


def ReceiveMessage():
    server_response = client.recv(1024)
    # Deserialize the data.
    server_data = pickle.loads(server_response)
    # Get all the values in the data dictionary
    client_id = server_data['client_id']  # the client id assigned by the server
    server_msg = server_data['msg']
    print("Client " + str(client_id) + "successfully connected to server")
    print("Server says: " + server_msg)


try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connects to the server using its host IP and port
    client.connect((HOST, PORT))

    while True:
        SendMessage(1, input("Enter Message: "))
        ReceiveMessage()

except socket.error as socket_exception:
    print(socket_exception)  # An exception occurred at this point
client.close()
