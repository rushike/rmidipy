import matplotlib.pyplot as plt
from rmidi import MIDI 

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