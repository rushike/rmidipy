
from .byte_block import ByteBlock

"""
Byte Chunk in top level break down for MIDI file
e.g. MTdh, MTrk chunks are stored in ByteChunk
It has length property which defines it size, property imediately follows after header
"""
class ByteChunk : 
    def __init__(self):
        self.header = None
        self.length = None
        self.content = bytes()
        self.block = []