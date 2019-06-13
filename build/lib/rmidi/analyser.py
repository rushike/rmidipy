import matplotlib.pyplot as plt
from rmidi.MIDI import MIDI
from rmidi.mutils import channel as mchannel

class Analyser:
    def __init__(self, midi_file, **kwargs):
        self.__midi = MIDI.parse_midi(midi_file)
        
    def stats(self):
        stat_freq = {'channel' : {8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0},
             'meta': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 32: 0, 33: 0, 47: 0, 81: 0, 84: 0, 88: 0, 89: 0, 127: 0}, 
             'sys': {240: 0, 247: 0}
             }
        for t in self.__midi.tracks:
            for e in t.trk_event:
                if e.is_channel_event():
                    stat_freq['channel'][mchannel(e.evt_id)] += 1
                elif e.is_meta_event():
                    stat_freq['meta'][e.meta_event_type] += 1
                elif e.is_meta_event():
                    stat_freq['sys'][e.event_id] += 1
                else : raise AttributeError('invalid MIDI event or Event Id got is not supported by this version of rmidi ')




if __name__ == "__main__":
    f = "./midis/Believer_-_Imagine_Dragons.mid"

    y = MIDI.parse_midi(f)

    t0 = y.track(0)

    n = t0.notes()
    nn = n["note_series"]
    x = [v[0] for v in nn]

    y = [v[1] for v in nn]

    plt.plot(x, y)
    plt.legend()
    plt.show()
