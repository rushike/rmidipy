import unittest
from rmidi.model.midi.midi import Midi

from rmidi.parser.parser import MIDI

import json

class ParserTest(unittest.TestCase):
    def setUp(self):
        filepath = "test.mid"
        
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_midi(self):
        filepath = "test.mid"
        midi_parser = MIDI.fromfile(filepath=filepath)
        midi = midi_parser.parse()
        # print(json.dumps(json.loads(str(midi)), indent=4))
        # print(str(midi))