from rmidi.constants import BIG_ENDIAN


class Reader:
    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs
        self.content = kwargs.get("content", bytes(0))
        self.iter = 0

    def read(self, rtype = "file"):
        if rtype == "file" : return FileReader(self.kwargs["filepath"])
        elif rtype == "buffer" : return self

    def next(self, length = 4): # return raw byte array
        try : 
            self.iter += length
            return self.content[self.iter - length: self.iter]
        except Exception as e:
            self.iter -= length
            raise EOFError(f"No more bytes to read. Can't read {length} number of bytes")

    def at(self, start = 0, length = 4):
        try :
            return self.content[start : start + length]
        except Exception as e:
            raise EOFError(f"No more bytes to read. Can't read at {start} with {length} number of bytes")
    
    def string(self, length = 4, format = BIG_ENDIAN, encoding = "UTF-8"): # retrun string instead raw bytes
        strbytes = self.next(length)
        return strbytes.decode(encoding)

    def number(self, arr = 4, mask = 0xff, format = BIG_ENDIAN, signed = False, dtype = int): # return number encoded in raw bytes
        if (type(arr) == int) : arr = self.next(arr)
        intnumber = self.masked(arr, mask)
        return int.from_bytes(intnumber, format, signed=signed)

    def masked(self, arr, mask = 0xff):
        return bytes(v & mask for v in arr)
        

class FileReader(Reader):
    def __init__(self, filepath) -> None:
        super().__init__()
        self.filepath = filepath
        self.content = self.read_content()
    
    def read_content(self):
        with open(self.filepath, 'rb') as f:
            bytes_arr = f.read()
        return bytes_arr

class BufferReader(Reader):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)