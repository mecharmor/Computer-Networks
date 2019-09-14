import socket
import pickle
import datetime

Host = '127.0.0.1'  # localhost
Port = '12000'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 12000))
server.listen(5)
print("Server listening on port (" + str(Port) + ")")

while True:
    # client connected
    # we need to save the host ip address and client socket connected
    client_sock, addr = server.accept()  # need to put everything after this on a thread. it will block after this

    client_id = addr[1]  # addr[0] is the host ip address. client id assigned by server

    print("Client " + str(client_id) + " has connected!")

    # inner loop handles interaction between client and server
    while True:
        try:
            # retrieve data from client
            request_from_client = client_sock.recv(1024)
            # deserialize data
            data = pickle.loads(request_from_client)
            # extract data from msg
            client_msg = data['msg_from_client']
            date = data['sent_on']

            # output result
            print("Client says: " + client_msg + " date [" + str(date) + "] ")

            # prepare server response
            server_msg = "Hello from the server!"
            server_response = {"client_id": client_id, "msg_from_server": server_msg}

            # serialize data
            serialized_data = pickle.dumps(server_response)
            client_sock.send(serialized_data)

            # closing connection from client side
            client_sock.close()

        except socket.error as socket_exception:
            print(socket_exception)  # exception occurred

    server.close()
