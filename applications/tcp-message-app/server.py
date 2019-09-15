import socket
import pickle
import datetime
import threading


class Server:
    def __init__(self):
        self.history = {}

    def start_server(self):
        host = "localhost"
        port = 8008

        # build server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(5)
        print("IP Address: " + host)
        print("port listening: " + str(port) + "...")
        print("Waiting for connections...")

        # Event Loop
        while True:
            try:
                client_sock, addr = server.accept()  # Note: addr[0] is client IP, addr[1] is socket id
                threading.Thread(target=self.handle_connection, args=(client_sock, addr[1])).start()
            except socket.error as socket_exception:
                print(socket_exception)

    def handle_connection(self, client_socket, client_id):
        print("Client " + str(client_id) + " has connected")
        # inner loop handles the interaction between this client and the server
        while True:
            request_from_client = None
            try:
                request_from_client = client_socket.recv(1024)
            except socket.error as e:
                # error 10053 is when client unexpectedly drops connection
                if e.errno == 10053 or e.errno == 10054:
                    break
                else:
                    print(e)

            server_msg = "sample message"
            if request_from_client:
                # deserialize
                data = pickle.loads(request_from_client)
                # parse
                client_msg = data['msg']
                client_route = data['client_route']
                timestamp = data['timestamp']
                username = data['username']

                print("Client says: " + client_msg + " message sent on " + str(timestamp))

            server_response = {"msg": server_msg,
                               "timestamp": datetime.datetime.now(),
                               "client_route": client_route,
                               "client_id": client_id
                               }
            serialized_data = pickle.dumps(server_response)
            client_socket.send(serialized_data)

        client_socket.close()


Server_ = Server()
Server_.start_server()

# def addToHistory(client_id, data):
#     if client_id in History:
#         History[client_id].append(data)
#     else:
#         History[client_id] = data
#
#
# def getMessagesOfClient(client_id):
#     if client_id in History:
#         str = None
#         for i in History[client_id]:
#             str += i['timestamp'] + ": " + i['msg'] + "\n"
#
#         return
#     else:
#         return None


# server_msg = None
# if client_route == 3:
#     server_msg = getHistoryOfClient(client_id)

# if client_route == 1:
#
# # get user list
# elif client_route == 2:
#
# # sent a message
# elif client_route == 3:
# # get my messages
# elif client_route == 4:
# # create a new channel
# elif client_route == 5:
# # create chat in a channel with your friends
# elif client_route == 6:
#     # disconnect from server
#     print(client_id + " disconnected")
#     break
