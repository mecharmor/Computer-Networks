import pickle
import datetime
import socket
import threading
from threading import Lock


class TCPClientHandler:
    def __init__(self, client_ref, username):
        self.client = client_ref
        self.username = username
        self.disconnected = False
        self.lock = Lock()
        self.channel_running = False

    def is_disconnected(self):
        return self.disconnected

    def next_prompt(self):
        print("****** TCP Message App ******\n"
              "1. Get user list\n"
              "2. Sent a message\n"
              "3. Get my messages\n"
              "4. Create a new channel\n"
              "5. Join a channel with your friends\n"
              "6. Disconnect from server")
        try:
            return int(input("Your option <enter a number>:"))
        except ValueError:
            return -1

    def handle_menu_selection(self, menu_selection):

        if menu_selection == 1:
            self.send_message(menu_selection)
            user_list = self.receive_message()
            print("Users\n" + user_list['msg'])

        elif menu_selection == 2:
            message_to_send = input("Message >>")
            recipient = input("User ID recipient (e.g: 50922)>>")
            self.send_message(menu_selection, message_to_send, recipient)

        elif menu_selection == 3:
            self.send_message(menu_selection)
            data = self.receive_message()
            print("My Messages:")
            print(data['msg'])

        elif menu_selection == 4:
            # Create a new channel
            host = input("Enter the ip address of the new channel:")
            port = int(input("Enter the port to listen for new users:"))
            print("---------------- Channel -----------------\n type 'bye' to stop channel")
            channel_socket_list = []
            self.channel_running = True
            threading.Thread(target=self.create_new_channel, args=(host, port, channel_socket_list)).start()
            while True:
                _input = input()
                if _input.__eq__("bye"):
                    self.channel_running = False
                    try:
                        for _socket in channel_socket_list:
                            _socket.send(pickle.dumps({'TERMINATE', True}))
                    except socket.error:
                        pass
                    break
            self.channel.close()

        elif menu_selection == 5:
            # Chat in a channel with your friends
            host = input("Enter the ip address of the channel:")
            port = int(input("Enter the port for the channel:"))
            self.connect_to_channel(host, port)

        elif menu_selection == 6:
            # Disconnect from the server
            self.send_message(6)
            print("You Disconnected!")
            self.disconnected = True

    def create_new_channel(self, host, port, channel_socket_list):
        # build channel
        self.channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channel.bind((host, port))
        self.channel.listen(5)
        print("Channel Info:\nIP Address:" + host + "\nChannel client id:" + str(port))
        print("Waiting for users...")
        # Event Loop
        while self.channel_running:
            try:
                client_socket, addr = self.channel.accept()  # Note: addr[0] is client IP, addr[1] is socket id
                channel_socket_list.append(client_socket)  # save ref to all sockets
                threading.Thread(target=self.handle_channel_connection, args=(client_socket, addr[1], channel_socket_list)).start()
            except socket.error as socket_exception:
                print(socket_exception)
                break
        self.channel.close()

    # server side threaded per socket connection
    def handle_channel_connection(self, client_socket, user_id, channel_socket_list):
        def message_all_clients(_req):
            for _socket in channel_socket_list:  # send message to all connected clients
                if _socket != client_socket:  # don't message yourself
                    try:
                        _socket.send(_req)
                    except socket.error:
                        pass

        data_from_req = None
        while self.channel_running:
            try:
                req = client_socket.recv(1024)
                data_from_req = pickle.loads(req)
                print(data_from_req['user_name'] + ": " + data_from_req['msg'])
                message_all_clients(req)
            except socket.error as e:
                break
            except EOFError:
                break
        username = data_from_req['user_name']
        message_all_clients(pickle.dumps({'user_name': username, 'msg': "Disconnected"}))
        if self.channel_running:
            print("client " + str(user_id) + " (" + username + ") disconnected!")
        channel_socket_list.remove(client_socket)
        client_socket.close()

    # client side
    def connect_to_channel(self, host, port):
        channel_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        channel_connection.connect((host, port))
        print("Successfully joined channel. type message below")

        def receive_from_channel(channel, _):
            while True:
                try:
                    data = pickle.loads(channel.recv(1024))
                    if 'TERMINATE' in data:
                        print("Channel shutdown. type 'bye' to leave session")
                        break
                    print(data['user_name'] + ": " + data['msg'])
                except socket.error as _e:
                    break
                except EOFError:
                    break

        threading.Thread(target=receive_from_channel, args=(channel_connection, '_')).start()  # start thread so console still outputs
        try:
            def send_to_channel(message, username):
                res = {'msg': message, 'user_name': username}
                res_serialized = pickle.dumps(res)
                channel_connection.send(res_serialized)
            send_to_channel("Connected", self.username)  # send user connected message
            while True:
                user_input = input()
                send_to_channel(user_input, self.username)
                if user_input.__eq__("bye"):
                    break
        except socket.error as e:
            print(e)
            pass

        print("Disconnected from the channel")
        channel_connection.close()

    def send_message(self, menu_option, message="", recipient_id=None):
        data = {"msg": message,
                "timestamp": datetime.datetime.now().replace(second=0, microsecond=0),
                "menu_option": menu_option,
                "username": self.username
                }
        if recipient_id is not None:
            data.update({"recipient_id": recipient_id})
        data_serialized = pickle.dumps(data)
        self.client.send(data_serialized)

    def receive_message(self):
        server_response = self.client.recv(1024)
        return pickle.loads(server_response)
