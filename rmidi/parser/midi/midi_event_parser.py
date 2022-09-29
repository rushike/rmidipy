from rmidi.parser.midi.midi_parser import MidiParser
from rmidi.model.midi.midi_event import MidiEvent

class MidiEventParser(MidiParser):
    def __init__(self, o) :
        super().__init__()
        self.o = o

    def parse(self):
        super().parse()
        return MidiEvent(self.o)
