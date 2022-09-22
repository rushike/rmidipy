from tkinter.tix import Tree
import unittest
from rmidi.constants import MIDI_HEADER

from rmidi.parser.reader import Reader

class ReaderTest(unittest.TestCase):
    def setUp(self):
        filepath = "transpose_one.mid"
        reader = Reader(filepath = filepath)
        self.reader = reader.read()
        

    def tearDown(self) -> None:
        return super().tearDown()

    def test_next(self):
        bytesarr = self.reader.next(5)
        assert(len(bytesarr) == 5)

    def test_string(self):
        strarr = self.reader.string(4)
        assert(strarr == MIDI_HEADER)

    def test_number(self):
        self.reader.string(4)
        numarr = self.reader.number(4)
        numarr = self.reader.number(self.reader.at(4, 4))
        assert(numarr == 6)