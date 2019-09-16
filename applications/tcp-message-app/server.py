import socket
import pickle
import datetime
import threading
from threading import Lock
from collections import defaultdict


class Server:
    def __init__(self):
        self.connected_users = {}
        self.chat_history = defaultdict(list)
        self.lock = Lock()
        # Note to self: NEVER STORE client_socket here!!!

    def send_message(self, client_socket, server_msg, menu_option, client_id, username):
        res = {"msg": server_msg,
               "timestamp": datetime.datetime.now().replace(second=0, microsecond=0),
               "menu_option": menu_option,
               "client_id": client_id,
               "username": username
               }
        res_serialized = pickle.dumps(res)
        client_socket.send(res_serialized)

    def get_client_messages(self, client_id):
        msgs = ""
        if client_id in self.chat_history.keys():
            for m in self.chat_history[int(client_id)]:
                msgs += m + "\n"
        return msgs

    def disconnect_user(self, client_id):
        self.lock.acquire()
        try:
            self.chat_history.pop(client_id)  # delete chat history
            self.connected_users.pop(client_id)  # remove from connected users
        except KeyError:
            pass
        print("Client " + str(client_id) + " disconnected from this server")
        self.lock.release()

    def start_server(self):
        host = "localhost"
        port = 8008

        # build server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(5)
        print("IP Address: " + host)
        print("listening on port " + str(port) + " ...")
        print("Waiting for connections...")

        # Event Loop
        while True:
            try:
                client_sock, addr = server.accept()  # Note: addr[0] is client IP, addr[1] is socket id
                threading.Thread(target=self.handle_connection, args=(client_sock, addr[1])).start()
            except socket.error as socket_exception:
                print(socket_exception)

    def handle_connection(self, client_socket, client_id):
        while True:
            req = None
            try:
                req = client_socket.recv(1024)
            except socket.error as e:
                # error 10053 is when client unexpectedly drops connection
                if e.errno == 10053 or e.errno == 10054:
                    self.disconnect_user(client_id)
                    break
                else:
                    print(e)

            if req:
                # deserialize
                data_from_req = pickle.loads(req)

                # parse req
                client_msg = data_from_req['msg']
                menu_option = data_from_req['menu_option']
                timestamp = data_from_req['timestamp']
                username = data_from_req['username']

                # 0, is initial handshake (login?)
                if menu_option == 0:
                    print("Client " + str(client_id) + " has connected")
                    self.connected_users.update({int(client_id): username})
                    self.send_message(client_socket, "<NO MESSAGE>", menu_option, client_id, username)

                # 1, Get user list
                elif menu_option == 1:
                    print("List of users sent to client: " + str(client_id) + " (" + username + ")")
                    user_list = ""
                    for c_id, u_name in self.connected_users.items():
                        user_list += str(c_id) + " , (" + str(u_name) + ")\n"
                    self.send_message(client_socket, user_list, menu_option, client_id, username)

                # 2, Sent a Message
                elif menu_option == 2:
                    print("Client says: " + client_msg + " message sent on " + str(timestamp))
                    self.chat_history[client_id].append(str(timestamp) + ": " + str(client_msg) + " (from: " + str(username) + ")")
                    if "recipient_id" in data_from_req.keys():
                        recipient_id = int(data_from_req['recipient_id'])
                        self.chat_history[recipient_id].append(str(timestamp) + ": " + str(client_msg) + " (from: " + str(username) + ")")
                    else:
                        print("Message cannot send because user id (" + data_from_req['recipient_id'] + ") does not exist")

                # 3, Get my messages
                elif menu_option == 3:
                    print("List of messages sent to: " + str(client_id) + " (" + username + ")")
                    messages = self.get_client_messages(client_id)
                    self.send_message(client_socket, messages, menu_option, client_id, username)

                # 4, Create a new channel
                elif menu_option == 4:
                    no_error = "delete this after i implement new channel"

                # 5, Chat in a channel with your friends
                elif menu_option == 5:
                    no_error = "delete this after i implement new channel"

                # 6, Disconnect from server
                elif menu_option == 6:
                    self.disconnect_user(client_id)
                    break

        client_socket.close()


Server_ = Server()
Server_.start_server()

# server_msg = None
# if menu_option == 3:
#     server_msg = getHistoryOfClient(client_id)

# if menu_option == 1:
#
# # get user list
# elif menu_option == 2:
#
# # sent a message
# elif menu_option == 3:
# # get my messages
# elif menu_option == 4:
# # create a new channel
# elif menu_option == 5:
# # create chat in a channel with your friends
# elif menu_option == 6:
#     # disconnect from server
#     print(client_id + " disconnected")
#     break
