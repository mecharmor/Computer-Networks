# -*- coding: utf-8 -*-
""" The tracker
This file implements the Tracker class. The tracker has two main functionalities
 (1) A client connects to a tracker, and a tracker sends
all the peers ip addresses and ports connected to the swarm that are sharing
the same resource. Since a tracker can handle more than one swarm, then the
swarm needs to be identified with a id (i.e the file id that is being shared
in the swarm)
 (2) When a peers change status (become leechers or seeders) they must inform
 the tracker, so the tracker can update that info in the swarm where they are
 sharing the resource

"""
from server import Server
from swarm import Swarm
import threading
import pickle

class Tracker(Server):

    def __init__(self, ip_address = '127.0.0.1', port = 13000):
        Server.__init__(self, ip_address, port)
        self.port = port
        self.ip = ip_address
        self.swarms = [] # the list of swarms that this tracker keeps
        self.listen()

    def remove_swarm(self, resource_id):
        self.swarms = [s for s in self.swarms if s.resource_id() != resource_id]

    def change_peer_status(self, resource_id):
        """
        TODO: implement this method
        When a peers in a swarm report a change of status
        (leecher or seeder) then, get the swarm object from
        the swarm list, and update the status in the swarm of
        such peer.
        :param resource_id:
        :return: VOID
        """
        pass

    def handle_connection(self, conn, addr): # Override
        self.logging.log("tracker.py -> handle_connection", "client connected: " + str(addr[1]))
        self.clients.append((conn, addr))

        try:
            resource_id = self.receive(conn, 1024)["resource_id"] # get resource id from peer
            if not self.is_resource_in_swarm(resource_id):
                self.add_swarm(Swarm(resource_id)) # Create a swarm for this new resource
            self.add_peer_to_swarm(addr, resource_id)

            data = {"socket_id": str(addr[1]), "my_ip": str(addr[0]), "swarm": self.get_swarm(resource_id)} # create map containing swarm
            self.send(conn, data) # send init data to peer
        except KeyError as e:
            self.logging.log("tracker.py -> handle_connection", "a Peer just connected but something went wrong with the data" + str(addr[0]), 2, str(e))

    def is_resource_in_swarm(self, resource_id):
        for s in self.swarms:
            if s.resource_id == resource_id:
                return True
        return False
                
    def send_peers(self, peer_socket, resource_id): # implemented
        for s in self.swarms:
            if s.resource_id == resource_id: # [issue], assuming peer_socket is the physical socket
                serialized = pickle.loads(s)
                peer_socket.send(serialized)

    def add_swarm(self, swarm):
        self.swarms.append(swarm)

    def get_swarm(self, resource_id):
        for swarm in self.swarms:
            if swarm.resource_id == resource_id:
                return swarm
        return ""

    def add_peer_to_swarm(self, peer, resource_id):
        idx = 0
        for swarm in self.swarms:
            if swarm.resource_id == resource_id:
                swarm.add_peer(peer)
                self.swarms[idx] = swarm
            idx += 1
                



tracker = Tracker()