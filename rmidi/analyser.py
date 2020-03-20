import matplotlib.pyplot as plt
from rmidi import MIDI, constant
from rmidi.mutils import channel as mchannel
from rmidi import mutils
from rmidi import AbsoluteMidi
from rmidi.constant import converter
import glob, os
import numpy
# import music21

class Analyser:
    def __init__(self, midi_file, **kwargs):
        self.__midi = MIDI.parse_midi(midi_file)
        
    def stats(self, names = False):
        stat_freq = {'channel' : {8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0},
             'meta': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 32: 0, 33: 0, 47: 0, 81: 0, 84: 0, 88: 0, 89: 0, 127: 0}, 
             'sys': {240: 0, 247: 0}
             }
        for t in self.__midi.tracks:
            for e in t.trk_event:
                if e.is_channel_event():
                    stat_freq['channel'][mchannel(e.event_id)] += 1
                elif e.is_meta_event():
                    stat_freq['meta'][e.meta_event_type] += 1
                elif e.is_meta_event():
                    stat_freq['sys'][e.event_id] += 1
                else : raise AttributeError('invalid MIDI event or Event Id got is not supported by this version of rmidi ')
        if names:
            c_stat_freq = dict()
            evt_format = mutils.dictn(Constant.ch_event_format)
            c_stat_freq['channel'] = {evt_format[k][0] : v for k, v in stat_freq['channel'].items()}
            evt_format = mutils.dictn(Constant.meta_event_format)
            c_stat_freq['meta'] = {evt_format[k][0] : v for k, v in stat_freq['meta'].items()}            
            evt_format = mutils.dictn(Constant.sys_event_format)
            c_stat_freq['sys'] = {evt_format[k][0] : v for k, v in stat_freq['sys'].items()}
            return c_stat_freq
        return stat_freq 

    @classmethod
    def analyse_dataset(cls, folder_path, save = '.', st = 1, end = 100):
        files = mutils.get_all_midis(folder_path)
        zstats = {}
        ana = cls(files[0])
        res = ana.stats(True)
        try : 
            for k, v in res.items():
                zstats[k] = {}
                for ik , iv in v.items():
                    try:
                        zstats[k][ik] = iv
                    except Exception:
                        zstats[k][ik] = 0

            for f in files[st:end]:
                try:
                    ana = cls(f)
                    res = ana.stats(True)
                except Exception:
                    continue

                for k, v in res.items():
                    for ik , iv in v.items():
                        try:
                            zstats[k][ik] += iv
                        except Exception:
                            zstats[k][ik] = 0
                del ana
        except Exception:
            pass
        numpy.save(save + '\\_FST_' + str(st) + '_END_' + str(end) + '_NUMPYSTORE_DATSET_' + folder_path.split('\\')[-1], zstats)
        1 == 2

    def track_analysis(self, resolution = 32): #Instrument Based
        #probably may out of scale , strech or contraction may present at end
        amidi = AbsoluteMidi.to_abs_midi(self.__midi)
        # print(amidi)
        isec = 500 * (4 / resolution) #17.250  // In milliseconds
        
        # LEN = int((300 * 1000) // isec) # For 5 min (MAX) only
        LEN = 4800
        trackers = numpy.zeros(amidi.track_count)
        track_anas = converter.meta_event_format()
        res_set = {}
        for i, t in enumerate(amidi.tracks):
            instrument = t.get_event('instrument_name', depth = 1)
            try :
                ttempo = mutils.toint(t.get_event('set_tempo', depth = 1)[0].data, 8)
                tempo = ttempo
            except IndexError:
                pass
            res_arr =  numpy.zeros(LEN)
            res_set[instrument[0].data.decode("utf-8")  + " " + str(i)] = res_arr
            nit = 0 #numpy array iterator
            prev_oucr, dut = 0, 0
            # print(t.trk_event[-11 : -1])
            for e in t.trk_event:
                if e.is_note_on_off_event():
                    # print(e)
                    if prev_oucr == e.abstime: 
                        nit -= dut
                        # print(res_arr[nit: nit + dut])
                    dut = int(32 // mutils.nth_note(e.elength, tempo=tempo)) 
                    prev_oucr = e.abstime
                    res_arr[nit: nit + dut] += 1
                    # print(res_arr[nit: nit + dut])
                    nit += dut
            # print("--------------------------------------=============================----------------------------------")

        return res_set
            

if __name__ == "__main__":
    f = 'midis\\Believer_Imagine_Dragons'

    c = Analyser(f)

    g = c.stats()

    c == g