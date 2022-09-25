from rmidi.constants import MIDI_HEADER
from rmidi.model.common.base import BaseModel


class MidiHeader(BaseModel):
    def __init__(self, header = MIDI_HEADER, length = 6, format = 0, ntrks = 0, division = 0) -> None:
        self.chunk_type = self.validate(header, MIDI_HEADER)
        self.length = self.validate(length, 6)
        self.format = self.validatein(format, [0, 1, 2])
        self.ntrks = ntrks
        self.division = division