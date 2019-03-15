from Event import Event
from MIDI import MIDI
from Constant import Constant
import mutils


class Track:
    def __init__(self, midi = MIDI()):
        self.id = 0
        self.length = 0
        self.trk_event = []
        self.midi_ = midi
        self.trk_event.append(Event.MetaEvent(0, 0x58,(0x4, 0x2, 0x18, 0x8))); #Meta Event : Time Signature
        self.trk_event.append(Event.MetaEvent(0, 0x59, (0x0, 0x0))); #Meta Event : Key Signature
        self.trk_event.append(Event.ChannelEvent(0, 0xb, 0x0, (79, 0))); #Channel Event : Controller  Blank Select
        self.trk_event.append(Event.ChannelEvent(0, 0xc, 0, (0x0))); #Channel Event : Program Change Event
        self.trk_event.append(Event.ChannelEvent(0, 0xb, 0, (0x7, 0x64))); #Channel Event : Controller  Main Volume
        self.trk_event.append(Event.ChannelEvent(0, 0xb, 0, (0x0a, 0x40))); #Channel Event : Controller  Pan
        self.trk_event.append(Event.ChannelEvent(0, 0xb, 0, (0x5b, 0x00)));#/Channel Event : Controller  External Effects Depth
        self.trk_event.append(Event.ChannelEvent(0, 0xb, 0, (0x5d, 0x00))); #Channel Event : Controller  formerly Chorus Depth
        self.trk_event.append(Event.MetaEvent(0, 0x21,(0x01, 0x00))); # Meta Event : Midi Port/ Should be prior to anyone
        self.trk_event.append(Event.MetaEvent(0, 0x2f, None)); #Meta Event : End of Track
    
    def _add_event(self, note, length, evt_id_byt, evt_stype = None, param = ()):
        return None
    def push_note(self, note_length, note_val, channel_no = 0, intensity = 0x50):
        end = self.trk_event.pop()
        self.trk_event.append(Event.ChannelEvent(self.delta_time(note_length), 0x9, channel_no, (note_val, intensity)))
        self.trk_event.append(end)

    def close_note(self, note_length, note_val, channel_no):
        end = self.trk_event.pop()
        self.trk_event.append(Event.ChannelEvent(self.delta_time(note_length), 0x8, channel_no, (note_val, 0x30)))
        self.trk_event.append(end)
    
    def delta_time(self, note_length):#Computes the delta time from tradition note duration, full, half, quater 
        if not note_length: return 0
        return (self.midi_.time_div * note_length ) // note_length
    
    def leng(self):#Returns length in bytes
        szn = 0
        for e in self.trk_event:
            szn += e.leng()
        return szn
    
    def to_byte_array(self):
        byte_list = bytearray()
        byte_list.append(Constant.Mtrk)
        # byte_list.append([0] * 4)
        for e in self.trk_event:
            byte_list.append(e.to_byte_array())
        byte_list.insert(4, mutils.to_fix_length(self.leng(), 4, 8))
        return byte_list