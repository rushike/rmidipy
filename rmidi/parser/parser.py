from __future__ import division
from rmidi.model.common.byte_chunk import ByteChunk
from rmidi.model.midi.midi import Midi
from rmidi.parser.midi.midi_header_parser import MidiHeaderParser
from rmidi.parser.midi.midi_track_parser import MidiTrackParser
from rmidi.parser.reader import Reader
from rmidiv1.MIDI import ch_event_id


class Parser:
    def __init__(self) -> None:
        pass

    def parse(self):
        pass



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
        header = self.reader.string(4) # should return midi header --> MTrk
        header_len = self.reader.number(4)
        chunk = ByteChunk(
            header=header, 
            length= header_len,
            content=self.reader.next(header_len)
            )
        return chunk.parse(MidiTrackParser)
    
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