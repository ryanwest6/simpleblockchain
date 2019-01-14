from hashlib import sha256
import time
import random


class Block:
    def __init__(self, index, prevHash, hash, timestamp, nonce, data):
        self.index = index
        self.prevHash = prevHash #deep copy this?
        self.hash = hash
        self.timestamp = timestamp,
        self.data = data
        self.nonce = nonce #necessary to keep all hashes unique

    def __str__(self):
        return 'Block ' + str(self.index) + ' with hash ' + str(self.hash.hexdigest())

    def toStringFull(self):
        return 'Block: ' + str(self.index) + \
               '\nHash: ' + str(self.hash.hexdigest()[:8]) + \
               '\nPrevious Hash: ' + str(self.prevHash.hexdigest()[:8]) + \
               '\nNonce: ' + str(self.nonce) + \
               '\nData: ' + str(self.data)
    # '\nTimestamp: ' + str(self.timestamp) + \



class Blockchain:

    def __init__(self):
        self.blocks = list()

    def add(self, data):
        prevHash = sha256('0'.encode('utf-8')) if len(self.blocks) == 0 else self.blocks[-1].hash
        nonce = str(random.randint(0, 100000000))
        hashData = str(data) + str(nonce)
        hash = sha256(hashData.encode('utf-8'))
        b = Block(len(self.blocks), prevHash, hash, time.ctime(), nonce, data.encode('utf-8'))
        self.blocks.append(b)

    def get(self, index):
        return self.blocks[index]

    def __len__(self):
        return len(self.blocks)


