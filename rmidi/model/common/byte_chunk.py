
from csv import reader

from rmidi.model.common.base import BaseByte
from rmidi.parser.reader import BufferReader
from .byte_block import ByteBlock

"""
Byte Chunk in top level break down for MIDI file
e.g. MTdh, MTrk chunks are stored in ByteChunk
It has length property which defines it size, property imediately follows after header
"""
class ByteChunk (BaseByte) : 
    def __init__(self, header = None, length = 0, content = bytes(), block = [], reader = None):
        self.header = header
        self.length = length
        self.content = content
        self.block = block
        self.reader = BufferReader(content = content)

    def parse(self, Parser):
        return Parser(self).parse()

    