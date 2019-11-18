# -*- coding: utf-8 -*-
""" The tracker
This file has the class swarm that represents a swarm
where peers can share a resource.
"""
class Swarm(object):

    def __init__(self, resource_id):
        self.peers = [] # the peers connected to this swarm
        self.resource_id = resource_id

    def add_peer(self, peer):
        self.peers.append(peer)

    def delete_peer(self, peer):
        self.peers.remove(peer)

    def peers(self):
        return self.peers

    def resource_id(self):
        return self.resource_id