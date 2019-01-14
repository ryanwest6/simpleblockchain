from hashlib import sha256
import time
import random


class Block:
    def __init__(self, index, prevHash, timestamp, nonce, data):
        self.index = index
        self.prevHash = prevHash #deep copy this?
        self.timestamp = timestamp,
        self.data = data
        self.nonce = nonce #necessary to keep all hashes unique

    def __str__(self):
        return 'Block ' + str(self.index) + ' with hash ' + str(self.hash.hexdigest())

    def toStringFull(self):
        return 'Block: ' + str(self.index) + \
               '\nHash: ' + str(self.hash())[:8] + \
               '\nPrevious Hash: ' + str(self.prevHash)[:8] + \
               '\nNonce: ' + str(self.nonce) + \
               '\nData: ' + str(self.data)
    # '\nTimestamp: ' + str(self.timestamp) + \

    # The block's hash is calculated as so: sha256(data + nonce)
    def hash(self):
        hashData = str(self.data) + str(self.nonce)
        return sha256(hashData.encode('utf-8')).hexdigest()

class MerkleRootTree:
    pass
    # next steps: figure out how to do the merkle root tree and add validation test 

class Blockchain:

    def __init__(self):
        self.blocks = list()


    def add(self, data):
        prevHash = sha256('0'.encode('utf-8')).hexdigest() if len(self.blocks) == 0 else self.blocks[-1].hash()
        nonce = str(random.randint(0, 100000000))
        b = Block(len(self.blocks), prevHash, time.ctime(), nonce, data.encode('utf-8'))
        self.blocks.append(b)

    def get(self, index):
        return self.blocks[index]

    def __len__(self):
        return len(self.blocks)


