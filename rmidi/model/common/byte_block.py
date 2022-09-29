
"""
ByteBlock stores the data in ByteChunk
It will have start and end define, or length property define in block itself
"""
from rmidi.model.common.base import BaseByte


class ByteBlock (BaseByte) : 
    def __init__(self, length, content, **kwargs):
        self.content = content
        self.length = length
        self.kwargs = kwargs

    
    def load(self, length, content, **kwargs):
        self.content = content
        self.length = length
        self.kwargs = kwargs
        