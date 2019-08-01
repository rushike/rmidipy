from rmidi.dataset import config
from rmidi import mutils
from rmidi.MIDI import MIDI
from rmidi.absolutemidi import AbsoluteMidi

class reader():
    def __init__(self, dataset_path = config.PATH):
        if not dataset_path: raise AttributeError("set config.PATH to dataset path, or specify the path value to attribute 'dataset_path'")
        config.PATH = dataset_path

    def read(self, abs_midi = False, generator = True):
        midis = mutils.get_all_midis(config.PATH)
        res = []
        for fmid in midis:
            mid = MIDI.parse_midi(fmid)
            if abs_midi: mid = AbsoluteMidi.to_abs_midi(mid)
            yield mid
            res.append(mid)
        return res