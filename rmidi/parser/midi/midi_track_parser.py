from distutils.log import error
from multiprocessing import Event
from tkinter import EventType
from rmidi.constants import MidiEventType, ChannelEventInfo
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
    
    def even_type(self, eventbyte, error = True):
        if eventbyte & 0x80 != 0x80 and error: raise AttributeError(f"Passed invalid attribute, event byte MSB bit should be 1, passed {eventbyte} with MSB {eventbyte & 0x80}")
        elif eventbyte == 0xff: return MidiEventType.META_EVENT
        elif eventbyte in (0xf0, 0xf7): return MidiEventType.SYS_EVENT
        elif ChannelEventInfo.ischannelevent(eventbyte) : return MidiEventType.CHANNEL_EVENT 
        else : return False

    def parse(self):
        super().parse()
        miditrack = MidiTrack(
            self.o, # tracks chunk
            self.o.header, # Track header : MTrk
            self.o.length, # tark length in bytes
            )
        iter = 0
        eventtype = -1
        while True:
            deltatime = self.o.reader.varlennumber()
            if eventtype == MidiEventType.CHANNEL_EVENT and not self.even_type(self.o.reader.head(1, True), error = False) :
                pass
            else :
                eventbyte = self.o.reader.next(1, True)
                eventtype = self.even_type(eventbyte)
    
            if eventtype == MidiEventType.META_EVENT:
                subeventbyte = self.o.reader.next(1, one = True)
                metaeventlen = self.o.reader.varlennumber()
                content = self.o.reader.next(metaeventlen)
                event = ByteBlock(
                                    metaeventlen, 
                                    content, 
                                    eventtype = eventtype, 
                                    eventbyte = eventbyte, 
                                    subeventbyte = subeventbyte, 
                                    deltatime = deltatime
                                ).parse(MidiEventParser)
                print("event : ", event)

                
            elif eventtype == MidiEventType.CHANNEL_EVENT:
                
                length = ChannelEventInfo.getlen(eventbyte)
                content = self.o.reader.next(length)
                event = ByteBlock(
                    length,
                    content,
                    eventtype = eventtype,
                    eventbyte = eventbyte,
                    deltatime = deltatime
                ).parse(MidiEventParser)
                
            elif eventtype == MidiEventType.SYS_EVENT:
                pass
            miditrack.add_event(event)
            iter += 1
            # break
            del content
            if eventtype == MidiEventType.META_EVENT and subeventbyte == 0x2f: break # End of Track Event
        return miditrack
