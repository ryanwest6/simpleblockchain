from hashlib import sha256
import time
import random
import math


class Ledger:

    class Block:
        def __init__(self, index, prevHash, timestamp, nonce, data):
            self.index = index
            self.prevHash = prevHash  # deep copy this?
            self.timestamp = timestamp,
            self.data = data
            self.nonce = nonce  # necessary to keep all hashes unique

        def __str__(self):
            return 'Block ' + str(self.index) + ' with hash ' + str(self.hash.hexdigest())

        def hash(self):
            return Ledger.hash(self)

        def toStringFull(self):
            return 'Block: ' + str(self.index) + \
                   '\tNonce: ' + str(self.nonce) + \
                   '\nHash: ' + str(self.hash())[:8] + \
                   ' PrevHash: ' + str(self.prevHash)[:8] + \
                   '\nData: ' + str(self.data)
            # '\nTimestamp: ' + str(self.timestamp) + \


    class MerkleTree:

        class Node:
            def __init__(self, lparent, rparent=None, hashVal=None):
                self.lparent = lparent
                self.rparent = rparent
                self.hashVal = hashVal
                if self.lparent is not None:
                    self.lparent.child = self
                self.rparent = None
                self.child = None
                if self.lparent is None:
                    self.height = 0
                else:
                    self.height = self.lparent.height + 1

            def hash(self):
                return self.hashVal

        def __init__(self):
            # if blocks == None or len(blocks) < 1:
            #     raise Exception("Error: At least one item must be provided")
            #self.is_built = False
            self.root_hash = None
            self.node_table = {}  # A map for intermediate nodes in the tree
            self.nodeLevels = [[]] # The same intermediate nodes, organized in a level fashion
            self.leaves = self.nodeLevels[0]  # The leaf nodes (one leaf per block of data)
            self.blocks = Ledger.Blockchain() # where the data is stored

        def get(self, index):
            return self.blocks.get(index)

        def __len__(self):
            return len(self.blocks)

        #def __getitem__(self, index):
        #    return self.blocks.blocks[index]

        def treeHeight(self):
            math.ceil(math.log(len(self.leaves), 2))

        # updates the branch of the last-added leaf according to parents
        def updateBranch(self, node):
            if node.rparent is not None:
                node.hashVal = Ledger.hash(node.lparent.hash() + node.rparent.hash())
            else:
                node.hashVal = Ledger.hash(node.lparent.hash())

            self.node_table[node.hashVal] = node

            # if num nodes on upper level is greater than half of nodes of current level, then this node has a
            # child already in the tree, so assign it
            # if node.child is None and len(self.nodeLevels) > node.height + 1 and len(self.nodeLevels[node.height]) / 2 >= len(self.nodeLevels[node.height+1]):
            #
            #     # if 5th leaf is being added, then level3 node 2 isn't created yet and must be added
            #     node.child = self.Node(lparent=node)
            #     self._addToNodeLevels(node.child)

                #node.child = self.nodeLevels[node.height+1][-1]
                #self.nodeLevels[node.height + 1][-1].rparent = node

            # recurse up branch until root or top is reached
            if node.child is not None:
                self.updateBranch(node.child)


        def add(self, data):
            self.blocks.add(data) # add the block to the blockchain
            self.leaves.append(self.Node(lparent=None, hashVal=self.blocks[-1].hash()))

            if len(self.leaves) == 6:
                print('d')

            # if there is one node with two parents
            if len(self.nodeLevels[0]) == 1:
                if self.nodeLevels[0][0].lparent is not None and self.nodeLevels[0][0].rparent is not None:
                    child = self.Node(self.nodeLevels[0][0],
                                      self.nodeLevels[0][0].hashVal)  # put node into tree with lparent specified
                    self.node_table[child.hashVal] = child
                    self._addToNodeLevels(child)
                    # self.nodeLevels[child.height][0].child = child

            for lvl in range(len(self.nodeLevels)):
                if len(self.nodeLevels[lvl]) <= 1:
                    pass
                # if odd number of leaves now, then make 1+ new nodes
                elif len(self.nodeLevels[lvl]) % 2 == 1:
                    # add node for new leaf
                    lparent = self.nodeLevels[lvl][-1]
                    child = self.Node(lparent)  # put node into tree with lparent specified
                    lparent.child = child
                    self._addToNodeLevels(child)  # TODO: this adds an idential node at lvl 1 node 6, need to add checking that another node doesn't already exist. perhaps combine this and update_branch
                    self.node_table[child.hashVal] = child  # keep block data in a map
                    self.updateBranch(lparent.child)

                # when even number of leaves now, we just complete the last node
                else:
                    lparent = self.nodeLevels[lvl][-2]
                    rparent = self.nodeLevels[lvl][-1]

                    if lparent.child is None:
                        child = self.Node(lparent=lparent, rparent=rparent, hashVal=self.blocks[-1].hash())
                        lparent.child = child
                        self._addToNodeLevels(child)
                    rparent.child = lparent.child
                    lparent.child.rparent = rparent  # all that's required is updating lparent's child's rparent
                    self.node_table[rparent.child.hashVal] = None  # delete old value
                    self.updateBranch(rparent.child)  # and then updating the branch accordingly

            print('Block added: ' + str(len(self.nodeLevels[0])))
            for i,lvl in enumerate(self.nodeLevels):
                print('Level ' + str(i) + ': ' + str(len(self.nodeLevels[i])))

        def _addToNodeLevels(self, child):
            if child.height >= len(self.nodeLevels):
                self.nodeLevels.append([])
            if child.height >= len(self.nodeLevels):
                raise Exception('height had to be raised more than once')
            self.nodeLevels[child.height].append(child)

        # def _buildTree(self):
        #     stack = []
        #     if len(self.leaves) == 1:
        #         solo_node = self.leaves.pop()
        #         self.root_hash = solo_node.hash
        #         self.node_table[solo_node.hash] = solo_node
        # 
        #     while self.root_hash == None:
        #         if len(stack) >= 2 and stack[-1].height == stack[-2].height:
        #             lparent = stack.pop()
        #             rparent = stack.pop()
        #             childHash = Ledger.hash(lparent.hash() + rparent.hash())
        #             child = self.Node(lparent, rparent, childHash)
        #             self.node_table[childHash] = child
        #             lparent.child = child
        #             rparent.child = child
        # 
        #             #if child.height == self.max_height:
        #             #    self.root_hash = child.hash
        # 
        #             stack.append(child)
        # 
        #         elif len(self.leaves) > 0:
        #             leaf = self.leaves.pop()
        #             self.node_table[leaf.hash] = leaf
        #             stack.append(leaf)
        #         # Handle case where last 2 nodes do not match in height by "graduating"
        #         # last node
        #         else:
        #             stack[-1].height += 1
        #     self.is_built = True

        # return the data blocks and intermediate merkle nodes required to validate that that
        # block resides in the merkle tree
        def buildMerkleProof(self, block):
            pass

        # gets the current merkle root value of the tree
        def getMerkleRoot(self):
            pass


    # simple list of blocks
    class Blockchain:

        def __init__(self):
            self.blocks = []

        def add(self, data):
            prevHash = sha256('0'.encode('utf-8')).hexdigest() if len(self.blocks) == 0 else self.blocks[-1].hash()
            nonce = str(random.randint(0, 100000000))
            b = Ledger.Block(len(self.blocks), prevHash, time.ctime(), nonce, data.encode('utf-8'))
            self.blocks.append(b)

        def get(self, index):
            return self.blocks[index]

        def __len__(self):
            return len(self.blocks)

        def __getitem__(self, index):
            return self.blocks[index]


    # init for Ledger
    def __init__(self, storageType):
        self.storage = storageType()

    # The block's hash is calculated as so: sha256(data + nonce)
    def hash(block):
        if isinstance(block, Ledger.Block):
            hashData = str(block.data) + str(block.nonce)
        else:
            hashData = str(block)
        return sha256(hashData.encode('utf-8')).hexdigest()



