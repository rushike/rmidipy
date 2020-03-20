from rmidi.dataset import config
from rmidi import mutils
from rmidi import MIDI
from rmidi import AbsoluteMidi
from rmidi.constant import converter
import numpy

class PianoRoll:
    def __init__(self, midi, print_threshold = 25):
        self.midi = midi
        self.print_threshold = print_threshold
        self.roll = None
        pass

    def pianoroll(self):
        if not isinstance(self.midi, AbsoluteMidi):
            self.midi = AbsoluteMidi.to_abs_midi(self.midi)
        LEN = 4800
        trackers = numpy.zeros(self.midi.track_count)
        track_anas = converter.meta_event_format()
        res_set = numpy.zeros((self.midi.track_count, 128, LEN))
        for i, t in enumerate(self.midi.tracks):
            instrument = t.get_event('instrument_name', depth = 1)
            try :
                ttempo = mutils.toint(t.get_event('set_tempo', depth = 1)[0].data, 8)
                tempo = ttempo
            except IndexError:
                pass
            nit = 0 #numpy array iterator
            prev_oucr, dut = 0, 0
            # print(t.trk_event[-11 : -1])
            for e in t.trk_event:
                if e.is_note_on_off_event():
                    # print(e)
                    if prev_oucr == e.abstime: 
                        nit -= dut
                    noteval = e.data[0]
                    dut = int(32 // mutils.nth_note(e.elength, tempo=tempo)) 
                    prev_oucr = e.abstime
                    res_set[i][noteval][nit: nit + dut] += 1
                    nit += dut
        self.roll = res_set
        return res_set

    def to_str(self, res = None):
        p_str = ""
        tracks, notes, intervals = numpy.shape(self.roll)
        for t in range(tracks):
            for n in range(notes):
                p_str += mutils.midi_to_note(n) + " : "
                for i in  range(self.print_threshold):
                    p_str += ( str(self.roll[t][n][i]) + " -- " )

                p_str += "\n"

            p_str += "************************ NEW TRACK ***************************************************** NEW TRACK *********************************"
        return p_str
        
    def __repr__(self):
        p_str = ""
        tracks, notes, intervals = numpy.shape(self.roll)
        for t in range(tracks):
            for n in range(notes):
                p_str += mutils.midi_to_note(n) + " : "
                for i in  range(self.print_threshold):
                    p_str += ( str(self.roll[t][n][i]) + " -- " )

                p_str += "\n"

            p_str += "************************ NEW TRACK ***************************************************** NEW TRACK *********************************"
        return p_str
            
            

         