from rmidi import *
import math, itertools
from rmidi import mutils
class Muse:

    def __init__(self, *args, **krgws):
        return
    
    def sequence(self, length, start = 0, sequence = 'fibonacci', modulo = 88, **kwargs):
        seq = [0] * length
        for i in range(length):
            seq[i] = int(1 / math.sqrt(5) * (math.pow((1 + math.sqrt(5)) / 2, i + 1) - math.pow((1 - math.sqrt(5)) / 2, i + 1)))
            while 60 < seq[i] and seq[i] > 88: 
                seq[i] += 48
                seq[i] = seq[i] % modulo
            # print("seq : ", seq[i])

        return seq
    def muse(self, dtime, notes, time_div = 0x1e0):
        m = MIDI(format_type= 1, track_count = 1, time_div=time_div)
        for i in range(len(dtime)):
            # print("tm, nt = ", dtime[i], notes[i])
            m.track(0).add_event(0, 'note_on', note_number = notes[i], velocity = 90, channel_no = 0)
            m.track(0).add_event(dtime[i], 'note_on', note_number = notes[i], velocity = 0, channel_no = 0)
        return m