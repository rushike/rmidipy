from __future__ import division
from rmidi.model.common.byte_chunk import ByteChunk
from rmidi.model.midi.midi import Midi
from rmidi.model.midi.midi_header import MidiHeader
from rmidi.parser.reader import Reader


class Parser:
    def __init__(self) -> None:
        pass

    def parse(self):
        pass


class MidiParser:
    def __init__(self) -> None:
        pass
    def parse(self):
        pass

class MidiHeaderParser(MidiParser):
    def __init__(self, o) -> None:
        super().__init__()
        self.o = o
    def parse_division(self, bytearr = bytes([0x01, 0xe0])):
        if len(bytearr) != 2: raise AttributeError( f"Passed invalid attribute, bytearr : {bytearr}")
        if bytearr[0] & 0x7f == 0x7f : #  SMPTE and MIDI Time Code. 
            return bytearr
        elif bytearr[0] & 0x80 == 0 : # delta time ticks
            return self.o.reader.number(bytearr)

    def parse(self):
        super().parse()
        format = self.o.reader.number(2)
        ntrks = self.o.reader.number(2)
        division = self.parse_division(self.o.reader.next(2))
        return MidiHeader(
            header=self.o.header,
            length=self.o.length,
            format= format,
            ntrks=ntrks,
            division=division
            )


class MIDI (Parser): 
    """ Offline Midi Processing
    """
    def __init__(self, filepath, reader): 
        self.filepath = filepath
        self.reader = reader
        self.struct = [
            {
                "name" : "header",
                "type" : "Object"
            },
            {
                "name" : "tracks",
                "type" : "Array"
            }
        ]

    def parse_header(self):
        header = self.reader.string(4) # should return midi header --> MThd
        header_len = self.reader.number(4) # should return --> 6
        chunk = ByteChunk(
            header=header, 
            length= header_len,
            content=self.reader.next(header_len)
            )

        return chunk.parse(MidiHeaderParser)
    
    def parse_tracks(self):
        return None

    def parse(self):
        super().parse()
        midi = None
        for block in self.struct:
            if block["name"] == "header" :
                midi = Midi(self.parse_header())
            elif block["name"] == "tracks" :
                self.parse_tracks()
        return midi

    @classmethod
    def fromfile(cls, filepath) :
        reader = Reader(filepath = filepath).read()
        return cls(filepath, reader)    

class MIDIStream :
    """ Online Midi Processing
    """
    def __init__(self):
        pass