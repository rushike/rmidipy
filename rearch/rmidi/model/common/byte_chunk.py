
from .byte_block import ByteBlock

class ByteChunk : 
    def __init__(self):
        self.header = ByteBlock()
        self.body = ByteBlock()