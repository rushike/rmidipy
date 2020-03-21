from rmidi import mutils
from rmidi import MIDI
from rmidi import AbsoluteMidi
from rmidi import rmidix
from rmidi import analyser
import numpy, random
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from rmidi.dataset import piano_roll
'''
MIDI Object Testing
'''
import os

def test_open_midi_file(filename = 'check.mid'):
    y = MIDI.parse_midi(filename)
    print(y)
# test_open_midi_file()

'''
Sequence
'''
# mu = rmidi.Muse()
# le = 7
# x = numpy.arange(12, 12 + le, 2)
# se = [1, 2, 4, 8, 16, 32]
# x = [random.choice(se) for i in range(le)]
# y = mu.sequence(le)
# m = mu.muse(x, y)
# print(m)


# m.create_file("test_add_event_ch")
# m.compress("test_add_event_ch")
# c = m.parse_midi('test-legit.mid')
# print(c)
# # c.create_file('duplicate')
# c.compress()


"""
midi_to_note testing from mutuls 
21 -> c0
60 -> c4
"""
def test_midi_to_note(number = 60, array = [56, 56, 78, 98, 34, 54, 95]):
    y = mutils.midi_to_note(array)
    y2 = mutils.midi_to_note(number)
    print(f"array conversion {y}, number conversion {y2}")
# test_midi_to_note()

"""
Testing the set_tempo of MIDI
"""
def test_midi_tempo_change(filepath = './rmidi/default.mid'):
    x = MIDI.parse_midi(filepath)
    x.track(0).set_tempo(0, 256)
    notes = [56, 58, 60, 61, 63, 65, 67, 68]
    dtime = 1
    for i in range(len(notes)):
        x.track(0).add_event(0, 'note_on', note_number = notes[i], velocity = 90, channel_no = 0)
        x.track(0).add_event(dtime, 'note_on', note_number = notes[i], velocity = 0, channel_no = 0)
            
    x.compress('../dataset/midi_gen/tempo_change')


"""
Sieve Erothenes 
"""

# import numpy, math
# def such(n):
#     nums = numpy.zeros(1000000, dtype = numpy.int32)
#     primes = [2]
#     i = 0
#     while primes[i] < math.sqrt(1000000) :
#         for j in range( primes[i], 1000000, primes[i]):
#             if nums[j] == 0:  nums[j] = primes[i]
#         for j in range(primes[i] + 1, 2 * primes[i]):
#             if nums[j] == 0:
#                 primes.append(j)
#                 break
#         i += 1
#     nums
#     return nums

# a = such(10)
# unique, counts = numpy.unique(a, return_counts=True)
# dct = dict(zip(unique, counts))
# n = 11
# pp = dct[n]

# print(pp)


'''
Test Analyser
'''
# f = 'rmidi\default.mid'

# c = analyser.Analyser(f)

# g = c.stats(True)

# g = analyser.Analyser.analyse_dataset('..\\dataset\\lakh_dataset', save='..\\dataset\\numpy', end = 1000)

# np = numpy
# g = np.load('F:\\rushikesh\\project\\dataset\\numpy\\_FST_1_END_1000_NUMPYSTORE_DATSET_lakh_dataset.npy')
# g = g.item()
# print(g)
# sm = 0
# for k, v in g['channel'].items():
#     sm += v
# print('\n\n-------------------------------------------------\n\npercent : ', (g['channel']['pitch_bend']/sm * 100))
# # g['channel']
# fig = plt.figure(tight_layout=True)
# gs = gridspec.GridSpec(2, 2)

# ax = fig.add_subplot(gs[0, :])
# cx , cy = list(g['channel'].keys()), list(g['channel'].values())
# ax.bar(cx[2:], cy[2:])
# ax.set_ylabel('frequency of occurence')
# ax.set_xlabel('channel event')
# # plt.show()
# v = ['meta', 'sys']
# for i in range(2):
#     ax = fig.add_subplot(gs[1, i])
#     ax.bar(g[v[i]].keys(), g[v[i]].values())
#     ax.set_ylabel('%s event' % v[i])
#     ax.set_xlabel('%s event' % v[i])
#     if i == 0:
#         for tick in ax.get_xticklabels():
#             tick.set_rotation(55)
# fig.align_labels()  # same as fig.align_xlabels(); fig.align_ylabels()

# plt.show()


'''
Testing get event method, Track class

'''
# f = '..\\dataset\\midi_gen\\tempo_change.mid'

# g = MIDI.parse_midi(f)

# ev = g.track(0).get_event('set_tempo')
# print(ev)
# 1 == 0


'''
Testing AbsMIDI
'''
# f = '..\\dataset\\midi_gen\\tempo_change.mid'
# f = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'

# g = MIDI.parse_midi(f)
def test_abs_midi(filepath = 'check.mid'):
    y = MIDI.parse_midi(filepath)
    abst = AbsoluteMidi.to_abs_midi(y)
    sbty = abs(y)
    print(abst)
    print(sbty)

'''
Testing Track Analysis from analyser, Can extend to multiple midi
# '''
# fi = '..\\dataset\\midi_gen\\tempo_change.mid'
# fi = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'

# ana = analyser.Analyser(fi)

# res = ana.track_analysis(resolution= 32)
# print(res)

# # g = []
# g = res
# fig = plt.figure(tight_layout=True)
# gs = gridspec.GridSpec(2, 2)

# ax = fig.add_subplot(gs[0, :])
# cx , cy = numpy.arange(len(g['Piano 0'])), g['Piano 0']
# ax.plot(cx[2:], cy[2:])
# ax.set_ylabel('frequency of note occurence')
# ax.set_xlabel('Piano 0')
# # plt.show()
# v = ['Piano 1', 'Piano 2']
# for i in range(2):
#     ax = fig.add_subplot(gs[1, i])
#     ax.plot(cx, g[v[i]])
#     ax.set_ylabel('Frequency of note occurence')
#     ax.set_xlabel('%s' % v[i])
#     if i == 0:
#         for tick in ax.get_xticklabels():
#             tick.set_rotation(55)
# fig.align_labels()  # same as fig.align_xlabels(); fig.align_ylabels()

# plt.show()

'''
nth note
'''
# fi = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'
# mid = MIDI.parse_midi(fi)    
# m = AbsoluteMidi.to_abs_midi(mid)
# print(m.tempo)
# t = mutils.nth_note(19.98905, m.tempo)

'''
piano roll testing
'''
# fi = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'
# mid = MIDI.parse_midi(fi) 
# numpy.set_printoptions(threshold=200)

# roll = piano_roll.PianoRoll(mid)

# roll_mat = roll.pianoroll()
# st = roll.to_str()
# print(st)
# print(len(st))
# 1 == 0

"""
transpose_to testing 
"""
# fi = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'
# mid = MIDI.parse_midi(fi) 
# numpy.set_printoptions(threshold=200)

# trans = mid.transpose_to('c-major')
# trans = mid.change_scale('a-major')
# print(trans.track(0).get_event('key_sig'))
# trans.create_file('transpose_one')

"""
note frequencies
"""
# fi = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'
# mid = MIDI.parse_midi(fi) 
# numpy.set_printoptions(threshold=200)

# freq_count = mid.note_frequencies()

# print(freq_count)

# fig = plt.figure(tight_layout=True)
# gs = gridspec.GridSpec(1, freq_count.shape[0])


# # plt.show()
# v = ['meta', 'sys']
# for i in range(2):
#     ax = fig.add_subplot(gs[0,i])
#     cx , cy = numpy.arange(256), freq_count[i]
#     ax.bar(cx, cy)
#     ax.set_ylabel('frequency of occurence')
#     ax.set_xlabel('midi notes')
#     if i == 0:
#         for tick in ax.get_xticklabels():
#             tick.set_rotation(55)
# fig.align_labels()  # same as fig.align_xlabels(); fig.align_ylabels()

# plt.show()


"""
testing array like indexing
m = MIDI.parse_midi(file_path)
track1 = m[0] 
"""
def test_array_like_indexing(filepath = 'check.mid'):
    m = MIDI.parse_midi(filepath)
    le = len(m) # getting length of midi(no. of tracks)
    for i in range(le):
        print(f"N:{i + 1}th = track : {m[0]}")
# test_array_like_indexing()


"""
Collating event format
"""
def test_event_format_struct():
    from  rmidi.constant import X
    print(X)
# test_event_format_struct()



"""
Testing NoteSequence
"""

def test_note_sequence(filepath = 'check.mid'):
    from rmidi.dataset import NoteSequence
    ns = NoteSequence(filepath)
    print(ns)
# test_note_sequence()

"""
To notes testing, ns.notes 
"""

def test_ns_notes(filepath = 'check.mid'):
    from rmidi.dataset import NoteSequence
    ns = NoteSequence(filepath)
    print(f"Notes : {ns.tostring(ns.notes)}")
# test_ns_notes()

"""
Order by testing of notesequence,
order by is intended to work to order_by , 'time', 'duration', 'pitch', deltatime 
only on work on notes 
"""
def test_order_by_ns(filepath = 'check.mid'):
    from rmidi.dataset import NoteSequence
    ns = NoteSequence(filepath)
    ordered = ns.order_by('pitch', reverse=True)
    print(f"order by attribute : time , seq : {ns.tostring(ordered)}")
# test_order_by_ns()

"""
NoteSequence to rmidi testing
"""
def test_ns_to_rmidi(filepath = 'check.mid'):
    from rmidi.dataset import NoteSequence
    ns = NoteSequence(filepath)
    absmidi = ns.to_abs_midi()
    print(absmidi)
test_ns_to_rmidi()
1 == 0