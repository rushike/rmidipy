
"""
ByteBlock stores the data in ByteChunk
It will have start and end define, or length property define in block itself
"""
class ByteBlock : 
    def __init__(self):
        self.content = None
        self.length = None

    
    def load(self, length, content):
        self.content = content
        self.length = length
        