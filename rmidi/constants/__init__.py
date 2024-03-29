from enum import Enum

from .midi_channel_event_info import ChannelEventInfo


BIG_ENDIAN = "big"
LITTLE_ENDIAN = "little"

MIDI_HEADER = "MThd"
MIDI_TRACK = "MTrk"

class MidiEventType(Enum):
    CHANNEL_EVENT = 0
    META_EVENT = 1
    SYS_EVENT = 2

