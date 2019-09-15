# Server implementation

# a) take ip and port as parameters. once executed wait listening at that port for new connections
# b) log connections
# c) log ALL activity to console
# d) server should never crash. use exception handling

import socket
import pickle
import datetime
import threading

lock = threading.Lock()

Host = "localhost"
Port = 8008
MAX_NUM_CONNECTIONS = 5
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((Host, Port))
server.listen(MAX_NUM_CONNECTIONS)  # max 5 connections at a time
print("Server listening at port: " + str(Port) + "... ")


def HandleConnection(_client_sock, _addr):
    # the client id assigned by server to this client
    # note that addr[0] is the host ip address
    _client_id = _addr[1]
    print("Client " + str(_client_id) + " has connected")
    # inner loop handles the interaction between this client and the server
    while True:
        # the server gets data request from client
        try:
            request_from_client = _client_sock.recv(1024)
        except socket.error as e:
            # error 10053 is when client unexpectedly drops connection
            if e.errno == 10053 or e.errno == 10054:
                break
            else:
                print(e)
        # deserialize the data
        if request_from_client:
            data = pickle.loads(request_from_client)
            client_msg = data['msg']
            client_setting = data['menu_selection']
            timestamp = data['timestamp']
            # disconnect
            if client_setting == 7:
                print(_client_id + " disconnected")
                break
            print("Client says: " + client_msg + " message sent on " + str(timestamp))  # crashing on this line!!!!!!!!!
        # prepare server response
        server_msg = "Hello from server!"
        server_response = {"client_id": _client_id, "msg": server_msg}
        # serialize and sent the data to client
        serialized_data = pickle.dumps(server_response)
        _client_sock.send(serialized_data)

    _client_sock.close()


# Event Loop
while True:
    try:
        client_sock, addr = server.accept()
        # thread handler
        threading.Thread(target=HandleConnection, args=(client_sock, addr)).start()

    except socket.error as socket_exception:
        print(socket_exception)

# join closed sessions
# for _t in activeThreads:
#     _t.join()
#     print(_t.getName() + "is joined")
# server.close()
