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
        return int(input("****** TCP Message App ******\n"
                         "1. Get user list\n"
                         "2. Sent a message\n"
                         "3. Get my messages\n"
                         "4.Create a new channel\n"
                         "5. Chat in a channel with your friends\n"
                         "6. Disconnect from server\n"
                         "Your option <enter a number>:"
                         ))

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
            delete_me_later = "removing errors by putting this message"
        elif menu_selection == 5:
            # Chat in a channel with your friends
            delete_this = "delete me when implementing"
        elif menu_selection == 6:
            # Disconnect from the server
            self.send_message(6)
            confirmed_disconnect = self.receive_message()
            if confirmed_disconnect['msg'] == "disconnected":
                print("You Disconnected!")
                self.disconnected = True

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
        try:
            server_response = self.client.recv(1024)
        except self.client.error as e:
            if e.errno == 10053 or e.errno == 10054:
                print("Server Connection Dropped!! (Server might be down)")
                print(e)
                exit()
        return pickle.loads(server_response)
