import time
import typing

CURRENT_VERSION = 0.1
class Block:
    """
    DOCTEST
>>> from blockchain import Block
>>> import time
>>> pre_start = time.time()
>>> blk = Block(0, 'previous_hash', 'data', 'signature')
>>> str(blk).startswith('<blockchain.Block object at ')
True
>>> blk.index, blk.previous_hash, blk.data, blk.signature, pre_start < blk.timestamp < time.time()
(0, 'previous_hash', 'data', 'signature', True)

>>> blk = Block(0, 'prev_hash', 'DATA', 'sig', 100)
>>> str(blk).startswith('<blockchain.Block object at ')
True
>>> blk.index, blk.previous_hash, blk.data, blk.signature, blk.timestamp
(0, 'prev_hash', 'DATA', 'sig', 100)


    """
    def __init__(self, index: int, previous_hash: str, data: str,
    signature: str, timestamp: float = None):
        """
        Constructor for the `Block` class.
        :param index:         Unique ID of the block.
        :param previous_hash: Hash of the previous block in the chain which this block is part of.
        :param timestamp:     Time of generation of the block Default: currant timestamp.
        :param version:       version of this block. default: current version
        """
        self.index = index
        self.previous_hash = previous_hash # Adding the previous hash field
        self.data = data
        if timestamp == None:
            timestamp = time.time()
        self.timestamp = timestamp
        self.signature = signature

    def compute_hash(self):
        """
        Returns the hash of the block instance by first converting it
        into JSON string.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True) # The string equivalent also considers the previous_hash field now
        return sha256(block_string.encode()).hexdigest()

if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    blk = Block(0, 'previous_hash', 'data', signature'signature')
    pass