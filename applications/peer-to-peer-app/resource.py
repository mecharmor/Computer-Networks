# -*- coding: utf-8 -*-
""" The Resource, Piece and Block classes
This file contains the classes Resource, Piece and Block to provide
services and functionalities needed from a resource in a swarm.
"""
import hashlib
from logging import Logging
import json
import os


class Block(object):
    def __init__(self, data, block_id, piece_id, resource_id):
        self.data = data
        self.resource_id = resource_id
        self.piece_id = piece_id
        self.block_id = block_id

    def getData(self):
        return self.data
    def getBlockId(self):
        return self.block_id
    def getPieceId(self):
        return self.piece_id
    def getResourceId(self):
        return self.resource_id


class Piece(object):

    def __init__(self, data, piece_id, resource_id, hash_pieces):
        self.hash_pieces = hash_pieces # list
        self.data = str(data)
        self.resource_id = resource_id
        self.piece_id = piece_id
        self.completed = False
        self.blocks = []
        self._create_blocks()
        self.hash = self._hash_sha1()

    def _create_blocks(self, max_size=16):
        increment_amount = max_size * 1024

        if increment_amount > len(self.data):
            self.blocks.append(Block(self.data, 0, self.piece_id, self.resource_id))
        else:
            prev = 0
            for end in range(increment_amount, len(self.data), increment_amount):
                self.blocks.append(Block(self.data[prev:end], prev/increment_amount, self.piece_id, self.resource_id))
                prev = end

    def is_equal_to(self, piece):
        for hp in self.hash_pieces:
            if hp == piece.hash:
                return True
        return False

    def _hash_sha1(self, data=None):
        if not data:
            data = self.data
        hash_object = hashlib.sha1(data.encode())
        return hash_object.hexdigest()

    def get_hash(self):
        return self.hash

    def get_blocks(self):
        return self.blocks

    def is_completed(self):
        return self.completed

    def set_to_complete(self):
        self.completed = True

class Resource(object):

    def __init__(self, torrent_path, isSeeder = False):
        self.logging = Logging()
        self.torrent_path = torrent_path
        torrent = self.parse_metainfo(torrent_path)
        self.resource_id = torrent["info"]["name"]
        self.len = torrent["info"]["length"]
        self.max_piece_size = torrent["info"]["piece length"]
        self.sha_pieces = torrent["info"]["pieces"].replace("<hex>", "").replace("</hex>", "").split(' ')
        self.isSeeder = isSeeder
        self.file_path = "./files/"

        self.pieces = []
        self._create_pieces()  # creates the file's pieces

    def len(self):
        return self.len

    def name(self):
        return self.resource_id

    def _create_pieces(self):

        if self.isSeeder:
            with open(self.file_path + self.resource_id, 'rb') as f:
                idx = 0
                while True:
                    b = f.read(self.max_piece_size)
                    if not b:
                        break
                    self.pieces.append(Piece(b, idx, self.resource_id, self.sha_pieces))
                    idx += 1
        else:
            # need to create the file if we do not have it and write into it...
            pass

    def get_piece(self, index):
        return self.pieces[index]

    def sha1_hashes(self):
        hashes = []
        for p in self.sha_pieces:
            hashes.append(p.gethash())
        return hashes

    def parse_metainfo(self, file_path):
        try:
            torrent = open(file_path, 'r')
            torrent_json = json.loads(torrent.read())
            return torrent_json
        except FileNotFoundError as e:
            self.logging.log("resource.py -> parse_metainfo", "could not find torrent file", 3, str(e))
            print("Could not find torrent file")
        except Exception as e:
            print("could not parse json: " + str(e))


resrc = Resource("./metainfo/config.torrent", True) # Create Resource as Seeder test
