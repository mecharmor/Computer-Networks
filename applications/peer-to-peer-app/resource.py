# -*- coding: utf-8 -*-
""" The Resource, Piece and Block classes
This file contains the classes Resource, Piece and Block to provide
services and functionalities needed from a resource in a swarm.
"""
import hashlib

class Resource(object):
    """
    This class provides services to handle resources
    """
    def __init__(self, resource_id = 0, file_path = None, file_len = 0, piece_len = 0 ):
        self.logging = Logging()
        """
        TODO: complete the implementation of this constructor.
        :param resource_id: default 0
        :param file_path: default None
        :param file_len: default 0
        :param piece_len: default 0
        """
        self.file_path = file_path
        self.resource_id = resource_id
        self.len = file_len
        self.max_piece_size = piece_len
        self._create_pieces() # creates the file's pieces
        self.trackers = []
        self.completed = []  # the pieces that are already completed

    def add_tracker(self, ip_address, port):
        self.trackers.append(ip_address + ":" + str(port))

    def get_trackers(self):
        return self.trackers

    def len(self):
        return self.len

    def name(self):
        return None

    def _create_pieces(self):
        """
        TODO: Implement this method
        Private method.
        This method will divide the file in pieces (same size)
        with the only exception of the last piece which has
        the left over bytes.
        :return: VOID
        """
        self.pieces = [] # list of objects of pieces. (see Piece class)


    def get_piece(self, index):
        """
        Already Implemented
        :param piece_id:
        :return: the piece requested
        """
        return self.pieces[index]

    def sha1_hashes(self):
        """
        TODO: implement this method.
        In this method you need to return all the
        sha1 hashes from each piece of the file
        1. iterate over the pieces list
        2. For each piece get its sh1a hash
        3. Add that hash to the hashes list below
        4. return the hashes list
        """
        hashes = []
        return hashes

    def parse_metainfo(self, file_path):
        try:
            torrent = open(file_path, 'rb')
            torrent_json = json.loads(torrent.read())
            return torrent_json
        except FileNotFoundError as e:
            self.logging.log("resource.py -> parse_metainfo", "could not find torrent file", 3, str(e))
            print("Could not find torrent file")
        except Exception as e:
            print("could not parse json: " + str(e))


class Piece(object):
    """
    This class provides the services needed to handle pieces from a resource (file)
    """
    def __init__(self, data, piece_id, resource_id):
        self.data = data
        self.resource_id = resource_id
        self.piece_id = piece_id
        self._create_blocks()
        self.hash = self._hash_sha1()
        self.completed = False


    def _create_blocks(self, max_size = 16):
        converted_size = max_size * 1024

        """
        TODO: implement this method
        (1) It is important here to create small chucks of data
            (block) that can be shared without compromising the
            app performance. A max size of 16KB is recomended
        (2) Convert the max_size to bytes (max_size * 1024)
        (3) Divide the piece in blocks of the same size. For example,
            a piece should have 256 blocks or more each one of 16KB
        (4) Append blocks created to the blocks list below
        (5) Return the blocks
        :param max_size: 16 KB set by default
        :return: the blocks
        """
        self.blocks = []

    def is_equal_to(self, piece):
        """
        TODO: implement this method
        Check if two pieces are the same.
        Note that you need to check their sha1 hashes
        to confirm that they are the same piece. For example,
        if you completed the download of a piece from another peer,
        you'll need to check the sha1 hash of that piece against the
        all the sha1 of all the pieces in the .torrent file.
        If there is a match, then if the piece is not corrupted,
        and the piece is now complete. Otherwise, the peer will need
        to request the piece of the file again.
        :param piece: another piece
        :return:
        """
        return False

    # Below Are Implemented
    def _hash_sha1(self, data = None):
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


class Block(object):
    """
    This class implements all the services provided by a block from piece
    """
    def __init__(self, block_id, piece_id, resource_id):
        self.resource_id = resource_id
        self.piece_id = piece_id
        self.block_id = block_id

    # TODO: think about which methods you would implement in this class.


