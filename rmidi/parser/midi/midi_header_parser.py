
from rmidi.parser.midi.midi_parser import MidiParser
from rmidi.model.midi.midi_header import MidiHeader

class MidiHeaderParser(MidiParser):
    """
        <Header Chunk> = <chunk type><length><format><ntrks><division>

    Args:
        MidiParser (_type_): Super Class
    """
    def __init__(self, o) -> None:
        super().__init__(o)

    def parse_division(self, bytearr = bytes([0x01, 0xe0])):
        if len(bytearr) != 2: raise AttributeError( f"Passed invalid attribute, bytearr : {bytearr}")
        if bytearr[0] & 0x7f == 0x7f : #  SMPTE and MIDI Time Code. 
            return bytearr
        elif bytearr[0] & 0x80 == 0 : # delta time ticks
            return self.o.reader.number(bytearr)

    def parse(self):
        super().parse()
        format = self.o.reader.number(2)
        ntrks = self.o.reader.number(2)
        division = self.parse_division(self.o.reader.next(2))
        return MidiHeader(
            header=self.o.header,
            length=self.o.length,
            format= format,
            ntrks=ntrks,
            division=division
            )

