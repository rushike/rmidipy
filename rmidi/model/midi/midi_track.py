
from rmidi.constants import MIDI_TRACK
from rmidi.model.common.base import BaseModel
from rmidi.model.midi.midi_event import MidiEvent


class MidiTrack(BaseModel):
    def __init__(self, chunk, chunktype = MIDI_TRACK, length = 0, events = []):
        self.chunk = chunk
        self.chunktype = chunktype
        self.length = length
        self.events = events # its is array/list of MidiEvents
        self.timeline = {}

    def add_event(self, event : MidiEvent):
        self.events.append(event)
        return True