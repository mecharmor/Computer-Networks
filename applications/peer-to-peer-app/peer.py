# -*- coding: utf-8 -*-
""" The peer """
from server import Server
from logging import Logging
from client import Client
import json

class Peer(Client, Server):

    # status
    PEER = 0
    SEEDER = 1
    LEECHER = 2

    def __init__(self, max_upload_rate, max_download_rate):
        """
        TODO: implement the class constructor
        """
        Server.__init__(self) # inherites methods from Server class
        Client.__init__(self) # inherites methods from Client class
        self.status = self.PEER
        self.chocked = False
        self.interested = False
        self.max_download_rate = max_download_rate
        self.max_upload_rate = max_upload_rate
        self.logging = Logging()

    def connect_to_tracker(self, ip_address, port):
        self.connect(ip_address, port)
        return self.receive(self.max_download_rate) # return swarm

    def connect_to_swarm(self, swarm):
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
        pass

    def upload_rate(self):
        """
        TODO: implement this method
        Compute the actual upload rate using the formule from assignment docs
        This needs to be re-evaluated every 30 seconds approximatly
        :return: the new upload_rate
        """
        return 5 # sample data for now

    def download_rate(self):
        """
        TODO: implement this method
        Compute the actual download rate using the formule from assignment docs
        This needs to be re-evaluated every 30 seconds approximatly
        :return: the new download rate
        """
        return 5 # sample data for now

    def change_role(self, new_role):
        """
        TODO: implement this method
        When a peer is interested in downloading a pieces of
        a resource, and the seeder or leecher sharing the resource
        is not chocked, then the peer becomes a leecher. When the
        leecher already have all the completed files from the file
        it becomes a seeder.
        :param new_role: use class constants: PEER, SEEDER or LEECHER
        :return: VOID
        """
        pass

    def send_message(self, block, start_index = -1, end_index = -1):
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

    def recieve_message(self):
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
        pass

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


max_upl = 10000
max_down = 10000
torrent_name = 'config.torrent'
peer_ip = '127.0.0.1'
peer_port = 12001

# Start
peer = Peer(max_upl, max_down)
torrent = peer.get_metainfo('./metainfo/' + torrent_name)
tracker = torrent['announce'].split(':') # tracker info, 0 = ip, 1 = port
swarm = peer.connect_to_tracker(tracker[0], int(tracker[1]))
peer.connect_to_swarm(swarm)

print("\n***** P2P client App *****")
print("Peer Info: id: xxxxx, IP: " + peer_ip + ":" + str(peer_port))
print("Tracker/s info: IP: " + torrent['announce'])
print("Max download rate: " + str(max_down) + " b/s")
print("Max upload rate: " + str(max_upl) + " b/s")
