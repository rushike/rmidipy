from numpy import dtype
from rmidi.constants import MidiEventType
from rmidi.constants.midi_channel_event_info import ChannelEventInfo
from rmidi.constants.midi_meta_event_info import MidiMetaEventInfo
from rmidi.parser.midi.midi_parser import MidiParser
from rmidi.model.midi.midi_event import MidiEvent

class MidiEventParser(MidiParser):
    def __init__(self, o) :
        super().__init__(o)

    def parse_channelevent(self, deltatime, eventbyte, content):
        if not ChannelEventInfo.ischannelevent(eventbyte): raise AttributeError(f"Passed invalid attribute, eventbyte : {hex(eventbyte)} not a channel event header")
        
        MASK = ChannelEventInfo.getinfo(eventbyte)["mask"]
        name = ChannelEventInfo.getinfo(eventbyte)["name"]
        params = ChannelEventInfo.getinfo(eventbyte)["params"]
        # for index, key in enumerate(params):
        #     print("inex, key : ", index, key)
        kwargs = {key : content[index] & MASK for index, key in enumerate(params)}
        kwargs = {**kwargs, "name" : name}
        
        if ChannelEventInfo.iscontrollerevent(eventbyte): kwargs = {**kwargs, "subtype" : ChannelEventInfo.CONTROLLER}

        return MidiEvent(
            self.o, 
            deltatime, 
            MidiEventType.CHANNEL_EVENT, 
            content,
            **kwargs
            )

    def parse_metaevent(self, deltatime, eventbyte, subeventbyte, length, content):
        if not MidiMetaEventInfo.ismetaevent(eventbyte, subeventbyte): raise AttributeError(f"Passed invalid attribute, eventbyte : {hex(eventbyte)} not a meta event header")
        
        subtypeinfo = MidiMetaEventInfo.getinfo(subeventbyte)
        subtype = MidiMetaEventInfo.getinfo(subeventbyte)["type_name"]
        dtype = MidiMetaEventInfo.getinfo(subeventbyte)["dtype"]
        # if dtype == 'str': 
        #     maskedconntent = MidiMetaEventInfo.cast(bytes([
        #         value & MidiMetaEventInfo.getmask(subeventbyte, index)
        #         for index, value in enumerate(content)
        #     ]),
        #     dtype)
        # else : maskedconntent = bytes([
        #         MidiMetaEventInfo.cast(value & MidiMetaEventInfo.getmask(subeventbyte, index), dtype)
        #         for index, value in enumerate(content)
        #     ])

        maskedconntent = bytes([
            value & MidiMetaEventInfo.getmask(subeventbyte, index)
            for index, value in enumerate(content)
        ])
        
        kwargs = {"data" : maskedconntent, "subtype" : subtype, "length" : length, "dtype" : dtype}
        
        return MidiEvent(
            self.o,
            deltatime,
            MidiEventType.CHANNEL_EVENT, 
            content,
            **kwargs
        )

    def parse(self):
        super().parse()
        # print("eventtpye : ", self.o.kwargs["eventtype"], ",  eventbyte : ", hex(self.o.kwargs["eventbyte"]), ", content : ", self.o.content)
        if self.o.kwargs["eventtype"] == MidiEventType.CHANNEL_EVENT:
            return self.parse_channelevent(
                self.o.kwargs["deltatime"],
                self.o.kwargs["eventbyte"],
                self.o.content
            )
        elif self.o.kwargs["eventtype"] == MidiEventType.META_EVENT:
            return self.parse_metaevent(
                self.o.kwargs["deltatime"],
                self.o.kwargs["eventbyte"],
                self.o.kwargs["subeventbyte"],
                self.o.length,
                self.o.content
            )
        elif self.o.kwargs["eventtype"] == MidiEventType.SYS_EVENT:
            pass
        return MidiEvent(self.o, self.o.kwargs["eventtype"], self.o.content, self.o.kwargs)
