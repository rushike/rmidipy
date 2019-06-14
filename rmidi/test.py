from rmidi import mutils
from rmidi.MIDI import MIDI
from rmidi import rmidi 
from rmidi import analyser
import numpy, random

'''
MIDI Object Testinh
'''

# import os

# y = MIDI.parse_midi('./midis/Believer_-_Imagine_Dragons.mid')

# tr = y.track(0)

# no = tr.notes()



# y.compress('check')

# # y.create_file('check')

# e = mutils.file_hash('./midis/Believer_-_Imagine_Dragons.mid')

# d = mutils.file_hash('check.mid')

# print(e, ", ", d , " : ", e == d)


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
# y = mutils.midi_to_note([56, 56, 78, 98, 34, 54, 95])

# y2 = mutils.midi_to_note(60)

# y == y2

"""
Testing the set_tempo of MIDI
"""

# x = MIDI.parse_midi('default.mid')

# x.set_tempo(56)

# x.compress('tempo_change')


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
f = 'rmidi\default.mid'

c = analyser.Analyser(f)

g = c.stats()

c == g