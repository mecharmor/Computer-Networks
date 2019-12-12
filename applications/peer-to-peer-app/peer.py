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

    PORT = 5000 # used for local connection

    def __init__(self, max_upload_rate, max_download_rate):
        """
        TODO: implement the class constructor
        """
        Server.__init__(self, '127.0.0.1', self.PORT) # inherites methods from Server class COULD BE WRONG TO SET LISTENING IP TO 0.0.0.0
        Client.__init__(self) # inherites methods from Client class
        self.status = self.PEER
        self.chocked = False
        self.interested = False
        self.max_download_rate = max_download_rate
        self.max_upload_rate = max_upload_rate
        self.logging = Logging()
        self.swarm_clients = []

    def lanIP(self):
        try: 
            host_name = socket.gethostname() 
            host_ip = socket.gethostbyname(host_name)
            return host_ip
        except: 
            print("Unable to get Hostname and IP") 

        return "xxx.xxx.xxx.xxx"

    def start_download(self, torrent_name):
        torrent = self.get_metainfo('./metainfo/' + torrent_name)
        tracker = torrent['announce'].split(':') # tracker info, 0 = ip, 1 = port
        swarm = self.connect_to_tracker(tracker[0], int(tracker[1]))
        peer.connect_to_swarm(swarm)

        print("\n***** P2P client App *****")
        print("Peer Info: id: xxxxx, IP: " + self.lanIP() + ":" + str(self.PORT))
        print("Tracker/s info: IP: " + torrent['announce'])
        print("Max download rate: " + str(self.max_download_rate) + " b/s")
        print("Max upload rate: " + str(self.max_upload_rate) + " b/s")

    def connect_to_tracker(self, ip_address, port):
        self.connect(ip_address, port)
        return self.receive(self.max_download_rate) # return swarm

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
            msg = self.receive(conn, self.max_download_rate)

    def handle_single_peer_connection(self, connected_client):
        """
        TODO: implement this method
        This method will create a socket (TCP) connection
        with all the peers in the swarm sharing the requested
        resource.
        Take into consideration that even if you are connected
        to the swarm. You do not become a leecher until you set
        your status to interested, and at least one of the leechers
        or seeders in the swarm is not chocked.
        :param swarm: Swarm object returned from the tracker
        :return: VOID
        """
        while True:
            data = connected_client.receive(self.max_download_rate) # we check if the peer sends a message and is requesting some data
            connected_client.send(self.max_upload_rate) # we send the data we have to the requester peer

    def connect_to_swarm(self, swarm): # BROKEN
        return # REMOVE SOON
        list_of_peers = swarm.peers()

        cl_port = self.PORT + 1
        for i in range(5):
            if i < len(list_of_peers):
                client = Client()
                client.connnect(XXXXXXX, XXXXXXXX) # need to access swarm and get ip informatin of those nodes swarm[i] or swarm[i].info()
                self.swarm_clients.append(cl)
                threading._start_new_thread(self.handle_single_peer_connection, client)
                cl = Client()


    def upload_rate(self):
        #self.get_top_four_peers()....
        """
        TODO: implement this method
        Compute the actual upload rate using the formule from assignment docs
        This needs to be re-evaluated every 30 seconds approximatly
        :return: the new upload_rate
        """
        return 5 # sample data for now

    def download_rate(self):
        # self.get_top_four_peers()
        # calculate here

        """
        TODO: implement this method
        Compute the actual download rate using the formule from assignment docs
        This needs to be re-evaluated every 30 seconds approximatly
        :return: the new download rate
        """
        return 5 # sample data for now

    def get_top_four_peers(self):
        """
        TODO: implement this method
        Since we are implementing the 'tit-for-tat' algorithm
        which upload data to the top 4 peers in the swarm (max rate upload peers)
        then this method will inspect the swarm object returned by the tracker
        and will get the 4 top peers with highest upload rates. This method needs to
        be re-evaluated every 30 seconds.
        :return: a list of the 4 top peers in the swarm
        """
        self.top_four = []
        # your implementation here
        return self.top_four

    def verify_piece_downloaded(self, piece):
        """
        TODO: implement this method
        :param piece: the piece object of this piece
        :return: true if the piece is verified and is not corrupted, otherwisem, return false
        """
        return False

    # ALL BELOW ARE DONE
    def change_role(self, new_role):
        if new_role == PEER:
            self.status = PEER
        elif new_role == SEEDER:
            self.status = SEEDER
        elif new_role == LEECHER:
            self.status = LEECHER
        else:
            self.logging.log("peer.py -> change_role", "incorrect role to set: " + str(new_role), 3, str(e))

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

