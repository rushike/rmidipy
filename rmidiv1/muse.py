from rmidiv1 import *
import math, itertools
from rmidiv1 import mutils
from rmidiv1.math import generator

class Muse:
    def __init__(self, start, length, sequence, dtime, **kwargs):
        self.start = start
        self.length = length
        self.sequence = sequence
        self.dtime = dtime
        self.kwargs = kwargs

    def generate(self):
        print(self.start, self.length, self.sequence)
        notes = Muse.series(self.start, length = self.length, sequence = self.sequence)
        m = Muse.muse(self.dtime, notes, kind = self.kwargs.get('kind', 'sec'), oftype= self.kwargs.get('oftype', 'melody'))
        m.compress(self.kwargs.get('filename', 'default.mid'))

    @classmethod
    def series(cls, start = 0, length = 10, sequence = 'fibonacci', modulo = 128, **kwargs):
        return numpy.fromiter(generator[sequence](start, start + length), dtype=int) % 128
    
    @classmethod
    def muse(cls, dtime, notes, time_div = 0x1e0, kind = 'sec', oftype = 'harmony'):
        """

        Args:
            dtime (int | array like): integer or time seq
            notes (array like): notes array
            time_div (hexadecimal, optional): [description]. Defaults to 0x1e0.
            kind (str, optional): must be in ['note', 'sec']. Defaults to 'sec'.
            oftype (str, optional): must be in ['melody', 'harmony']. Defaults to 'harmony'.

        Returns:
            [type]: [description]
        """
        if isinstance(dtime, int) or isinstance(dtime, float):
            dtime = numpy.zeros(len(notes)) + dtime
        m = MIDI(format_type= 1, track_count = 1, time_div=time_div)
        for i in range(len(dtime)):
            m.track(0).add_event(0, 'note_on', note_number = notes[i], velocity = 90, channel_no = 0, kind = kind)
            if oftype.lower() in ['melody']: m.track(0).add_event(dtime[i], 'note_on', note_number = notes[i], velocity = 0, channel_no = 0, kind = kind)
        if oftype.lower() in ['harmony', 'harmonic']:
            for i in range(len(dtime)):
                m.track(0).add_event(dtime[i], 'note_on', note_number = notes[i], velocity = 0, channel_no = 0, kind = kind)
        return m
