class ByteBlock : 
    def __init__(self):
        self.body = None
        self.length = None
    
    def load(self, length, body):
        self.body = body
        self.length = length
    