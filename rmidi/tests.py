import random, math, numpy

from rmidi import muse
from rmidi.img import tests

def test_muse(start, length, dtime = 1, filename = f'muse-{random.randint(0, 100)}', sequence = 'serial', oftype = 'melody'):
    print(start, length, dtime)
    mu = muse.Muse(start, length, sequence, 1, kind = 'sec', filename = filename, oftype = oftype)
    mu.generate()
#   test_muse(0, 128, dtime = 1, oftype='harmony')
