import pickle
import datetime


class TCPClientHandler:
    def __init__(self, client_ref, username):
        self.client = client_ref
        self.username = username
        self.disconnected = False
    def is_disconnected(self):
        return self.disconnected

    def next_prompt(self):
        return int(input(""
                         "****** TCP Message App ******"
                         "1. Get user list"
                         "2. Sent a message"
                         "3. Get my messages"
                         "4. Create a new channel"
                         "5. Chat in a channel with your friends"
                         "6. Disconnect from server"
                         "Your option <enter a number>:"))

    def handle_menu_selection(self, menu_selection, message=None):
        if menu_selection == 1:
            self.send_message(1)
            user_list = self.receive_message()
            self.display_user_list(user_list)
        elif menu_selection == 2:
            self.send_message(menu_selection, message)
        elif menu_selection == 3:
            self.send_message(menu_selection)
            my_messages = self.receive_message()
            print(my_messages)
        elif menu_selection == 4:
            # Create a new channel
            delete_me_later = "removing errors by putting this message"
        elif menu_selection == 5:
            # Chat in a channel with your friends
            delete_this = "delete me when implementing"
        elif menu_selection == 6:
            # Disconnect from the server
            self.send_message(6)
            confirmed_disconnect = self.receive_message()
            if confirmed_disconnect['msg'] == "disconnected":
                print("Client Disconnected!")
                self.disconnected = True

    def display_user_list(self, user_list):
        for i in user_list:
            print(i)

    def send_message(self, client_route, message=""):
        data = {"msg": message, "timestamp": datetime.datetime.now(), "client_route": client_route,
                "username": self.username}
        data_serialized = pickle.dumps(data)
        self.client.send(data_serialized)

    def receive_message(self):
        server_response = self.client.recv(1024)
        return pickle.loads(server_response)
