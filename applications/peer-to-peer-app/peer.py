# -*- coding: utf-8 -*-
""" The peer """
from server import Server
from logging import Logging
from client import Client
import threading
import random
import json

class Peer(Client, Server):

    # status
    PEER = 0
    SEEDER = 1
    LEECHER = 2

    PORT = 5000  # used for local connection

    def __init__(self, max_upload_rate, max_download_rate):
        """
        TODO: implement the class constructor
        """
        Server.__init__(self, '127.0.0.1', self.PORT) # inherites methods from Server class COULD BE WRONG TO SET LISTENING IP TO 0.0.0.0
        threading.Thread(target=self.listen, args=())
        Client.__init__(self) # inherites methods from Client class
        self.status = self.PEER
        self.chocked = False
        self.interested = False
        self.max_download_rate = max_download_rate
        self.max_upload_rate = max_upload_rate
        self.logging = Logging()
        self.swarm_clients = []
        self.myIp = "x.x.x.x"
        self.mySocketId = "00000"

    def start_download(self, torrent_name):
        torrent = self.get_metainfo('./metainfo/' + torrent_name)
        tracker = torrent['announce'].split(':') # tracker info, 0 = ip, 1 = port
        swarm = self.connect_to_tracker(tracker[0], int(tracker[1]), torrent['info']['name'])
        self.connect_to_swarm(swarm)

        print("\n***** P2P client App *****")
        print("Peer Info: id: " + self.mySocketId + ", IP: " + self.myIp + ":" + str(self.PORT))
        print("Tracker/s info: IP: " + torrent['announce'])
        print("Max download rate: " + str(self.max_download_rate) + " b/s")
        print("Max upload rate: " + str(self.max_upload_rate) + " b/s")

    def connect_to_tracker(self, ip_address, port, resource_id):
        self.connect(ip_address, port)
        self.send({"resource_id": resource_id})
        initial_data = self.receive(1024)

        try:
            # set init data
            self.myIp = initial_data["my_ip"]
            self.mySocketId = initial_data["socket_id"]
            return initial_data["swarm"]
        except Exception as e:
            self.logging.log("peer.py -> connect_to_tracker", " data from tracker: " + str(initial_data), 3, str(e))
            exit()

    def send_message(self, block, start_index = -1, end_index = -1):

        # this function is invoked by one of the multithreaded functions. probably from handle_single_peer_connection
        """
        TODO: implement this method
        (1) Create a message object from the message class
        (2) Set all the properties of the message object
        (3) If the start index and end_index are not negative
            then, that means that the block needs to be sent
            in parts. implement that situations too.
        (4) Don't forget to check for exceptions with try-catch
            before sending messages. Also, don't forget to
            serialize the message object before being sent
        :param block: a block object from the Block class
        :param start_index: the start index (if any) of the data being sent
        :param end_index: the end index of the data being sent
        :return: VOID
        """
        pass

    # ========== THESE 2 FUNCTIONS BELOW ARE HOW WE WILL HANDLE CONNECTIONS TO THE ENTIRE SWARM ====================

    def handle_connection(self, conn, addr): # OVERRIDDEN FROM SERVER, (THREADED)
        # This function is the entry point for peers to send data so we will want to parse the message class to retrieve that data
        # this functin is already multithreaded so we can loop in here forever without any issues on blocking the main thread
        self.logging.log("peer.py -> override handle_connection", "client connected: " + str(addr[0]))
        self.clients.append((conn, addr))

        # if requested we need to send our upload/download rate in a message

        while True:
         """
        TODO: implement this method
        (1) recieve the message
        (2) inspect the message (i.e does it have payload)
        (4) If this was the last block of a piece, then you need
            to compare the piece with the sha1 from the torrent file
            if is the same hash, then you have a complete piece. So, set
            the piece object related to that piece to completed.
        (5) Save the piece data in the downloads file.
        (6) Start sharing the piece with other peers.
        :return: VOID
        """
            # msg = self.receive(conn, self.max_download_rate)

    def handle_single_peer_connection(self, connected_client, _):
        while True:
            data = connected_client.receive(self.max_download_rate) # we check if the peer sends a message and is requesting some data
            connected_client.send(self.max_upload_rate) # we send the data we have to the requester peer

    def connect_to_swarm(self, swarm):
        list_of_peers = swarm.getPeers() # [0] - IP, [1] socket id

        connected_peers = 1
        for p in list_of_peers:
            if connected_peers <= 5 and str(p[1]) != str(self.mySocketId): # prevent connecting to self (during testing)
                    cl = Client()
                    cl.connect(p[0], self.PORT + connected_peers)
                    threading.Thread(target=self.handle_single_peer_connection, args=(cl, "")).start()
                    self.swarm_clients.append(cl)
                    connected_peers += 1
            else:
                print("Ignored Peer connection due to max 5 connections or connecting to self by accident")

    def upload_rate(self):
        #self.get_top_four_peers()....
        return 5 # sample data for now

    def download_rate(self):
        # self.get_top_four_peers()
        # calculate here
        #  sample data for now
        return 5

    def get_top_four_peers(self):
        self.top_four = []
        return self.top_four

    def verify_piece_downloaded(self, piece):
        return piece.is_completed() and not piece.is_corrupted()

    # ALL BELOW ARE DONE
    def change_role(self, new_role):
        if new_role == self.PEER:
            self.status = self.PEER
        elif new_role == self.SEEDER:
            self.status = self.SEEDER
        elif new_role == self.LEECHER:
            self.status = self.LEECHER
        else:
            self.logging.log("peer.py -> change_role", "incorrect role to set: " + str(new_role))

    def get_metainfo(self, torrent_path):
        try:
            torrent = open(torrent_path, 'r')
            torrent_json = json.loads(torrent.read())
            return torrent_json
        except FileNotFoundError as e:
            self.logging.log("peer.py -> get_metainfo", "could not find torrent file", 3, str(e))
            print("Could not find torrent file")
        except Exception as e:
            print("could not parse json: " + str(e))
        
        print("no torrent found. Terminating immediately......")
        exit()

    def is_chocked(self):
        return self.chocked

    def is_interested(self):
        return self.interested

    def chocked(self):
        self.chocked = True

    def unchocked(self):
        self.chocked = False

    def interested(self):
        self.interested = True

    def not_interested(self):
        self.interested = False

max_upl = int(random.random()*10000)
max_down = int(random.random()*10000)
torrent_name = 'config.torrent'

peer = Peer(max_upl, max_down)
peer.start_download(torrent_name)

