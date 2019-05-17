import librosa
import numpy
import matplotlib.pyplot as plt

class Sound:
    def __init__(self, stream = None, sample_rate = 44100):
        self.sample_rate = sample_rate
        self.stream = stream if stream else numpy.zeros(sample_rate)
    @classmethod
    def load(cls, filename, sample_rate = 44100):
        y, sr = librosa.load(filename, sample_rate)
        return cls(y, sr) 

import librosa
x, sr = librosa.load('modi.mp3')

plt.figure(figsize=(14, 5))
librosa.display.waveplot(x, sr=sr)