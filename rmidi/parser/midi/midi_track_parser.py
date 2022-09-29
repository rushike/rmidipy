from rmidi.constants import MidiEventType
from rmidi.model.common.byte_block import ByteBlock
from rmidi.model.common.byte_chunk import ByteChunk
from rmidi.model.midi.midi_track import MidiTrack
from rmidi.parser.midi.midi_event_parser import MidiEventParser
from rmidi.parser.midi.midi_parser import MidiParser


class MidiTrackParser(MidiParser):
    """
        <Track Chunk> = <chunk type><length><MTrk event>+
    """
    def __init__(self, o : ByteChunk) -> None:
        super().__init__(o)
    
    def even_type(self, eventbyte):
        if eventbyte & 0x80 != 0x80 : raise AttributeError(f"Passed invalid attribute, event byte MSB bit should be 1, passed {eventbyte} with MSB {eventbyte & 0x80}")
        elif eventbyte == 0xff: return MidiEventType.META_EVENT
        elif eventbyte in (0xf0, 0xf7): return MidiEventType.SYS_EVENT
        else: return MidiEventType.CHANNEL_EVENT 

    def parse(self):
        super().parse()
        miditrack = MidiTrack(
            self.o, # tracks chunk
            self.o.header, # Track header : MTrk
            self.o.length, # tark length in bytes
            )
        iter = 0
        while True:
            deltatime = self.o.reader.varlennumber()
            eventbyte = self.o.reader.next(1, True)
            eventtype = self.even_type(eventbyte)
            if eventtype == MidiEventType.META_EVENT:
                metaeventtype = self.o.reader.next(1, one = True)
                metaeventlen = self.o.reader.varlennumber()
                content = self.o.reader.next(metaeventlen)
                print("track event  : ", deltatime, eventtype, metaeventtype, metaeventlen)
                block = ByteBlock(
                                    metaeventlen, 
                                    content, 
                                    eventtype = eventtype, 
                                    eventbyte = eventbyte, 
                                    metaeventtype = metaeventtype, 
                                    deltatime = deltatime
                                ).parse(MidiEventParser)
            iter += 1
            if iter == 10 : break
