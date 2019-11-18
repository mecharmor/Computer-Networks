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

class Tracker(Server):

    PORT = 13000
    IP_ADDRESS = "127.0.0.1"

    def __init__(self, ip_address = '127.0.0.1', port = 13000):
        """
        TODO: finish constructor implementation (if needed)
        If parameters ip_address and port are not set at the object creation time,
        you need to use the default IP address and the default port set in the class constants.
        :param ip_address:
        :param port:
        """
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

    def send_peers(self, peer_socket, resource_id):
        """
        TODO: implement this method
        Iterate the swarms list, and find the one which match with
        the resource id provided as a parameter. Then, serialize the
        swarm and send the swarm object to the peer requesting it.
        :param peer_socket: the peer socket that is requesting the info
        :param resource_id: the resource id to identify the swarm
               sharing this resource
        :return: VOID
        """
        pass


    # implemented
    def add_swarm(self, swarm):
        self.swarms.append(swarm)

    def add_peer_to_swarm(self, peer, resource_id):
        for i in self.swarms:
            if i.resource_id() == resource_id:
                self.swarms.add_peer(peer)

