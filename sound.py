import librosa
import numpy

class Sound:
    def __init__(self, stream = None, sample_rate = 44100):
        self.sample_rate = sample_rate
        self.stream = stream if stream else numpy.zeros(sample_rate)
    @classmethod
    def load(cls, filename, sample_rate = 44100):
        y, sr = librosa.load(filename, sample_rate)
        return cls(y, sr) 
        