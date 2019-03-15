import mutils
from rmidi import MIDI
import rmidi
import numpy, random
# m = MIDI(1, 1, 0x1e0)
# val = 72
# for _ in range(8):
#     # m.track(0).push_note(0, val, 0, 90)
#     # m.track(0).close_note(4, val, 0)
#     m.track(0).add_event(0, 'note_on', note_number = val, velocity = 90, channel_no = 0)
#     m.track(0).add_event(2, 'note_on', note_number = val, velocity = 0, channel_no = 0)
#     val = (val + 2) % 80
#     if val < 72 : val = 72 + val  
mu = rmidi.Muse()
le = 100
x = numpy.arange(12, 12 + le, 2)
se = [1, 2, 4, 8, 16, 32]
x = [random.choice(se) for i in range(le)]
y = mu.sequence(le)
m = mu.muse(x, y)
print(m)
# m.create_file("test_add_event_ch")
m.compress("test_add_event_ch")
# c = m.parse_midi('test-legit.mid')
# print(c)
# # c.create_file('duplicate')
# c.compress()