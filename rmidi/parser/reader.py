from rmidi.constants import BIG_ENDIAN, LITTLE_ENDIAN


class Reader:
    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs
        self.content = kwargs.get("content", bytes(0))
        self.iter = 0

    def read(self, rtype = "file"):
        if rtype == "file" : return FileReader(self.kwargs["filepath"])
        elif rtype == "buffer" : return self

    def rest(self) :
        return self.content[self.iter:]

    def next(self, length = 4, one = False): # return raw byte array
        try : 
            self.iter += length
            if length == 1 and one: return self.content[self.iter - length]
            else : return self.content[self.iter - length: self.iter]
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
    
    def varlennumber(self, bytearr = None, bits = 7, format = BIG_ENDIAN) -> int:
        """It will return the variable length number stored
            Strategy used is based on delta time encoding in MIDI messages
            Last 7 bits in each byte will carry info, 
            1 bits of every byte is set to 1 expect 1 bit of last byte is set to 0

            e.g. 
            8 bytes number      Variable Length encoding
            00000040	        40
            0000007F	        7F
            00000080	        81 00
            00002000	        C0 00
            00003FFF	        FF 7F
            00004000	        81 80 00
            00100000	        C0 80 00
            001FFFFF	        FF FF 7F
            00200000	        81 80 80 00
        Args:
            bytearr (_type_, optional): bytes array  Defaults to bytes(0).

        Returns:
            int: number
        """
        if not bytearr : bytearr = self.content
        NUM_MASK = (1 << bits) - 1 # it will extract number from bits stored
        SET_MASK = 1 << bits # it will extract info of control bit
        num = 0x00
        try:
            while True:
                if format == LITTLE_ENDIAN:
                    num = num | ((bytearr[self.iter] & NUM_MASK) << bits)
                elif format == BIG_ENDIAN:
                    num = (num << bits) | (bytearr[self.iter] & NUM_MASK)
                self.iter += 1
                if bytearr[self.iter - 1] & SET_MASK == 0: break
            return num
        except KeyError as e:
            raise AttributeError(f"Passed invalid attribute, bytearr as no var end byte with MSB set to 1 :  {bytearr[-1]} |  {e}")

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