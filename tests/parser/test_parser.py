import unittest
from rmidi.model.midi.midi import Midi

from rmidi.parser.parser import MIDI

class ParserTest(unittest.TestCase):
    def setUp(self):
        filepath = "transpose_one.mid"
        # midi = MIDI.fromfile(filepath)
        # print(midi)

    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_midi(self):
        filepath = "transpose_one.mid"
        midi_parser = MIDI.fromfile(filepath=filepath)
        midi = midi_parser.parse()
        print(str(midi))