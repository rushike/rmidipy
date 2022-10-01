
from rmidi.model.common.base import BaseModel


class Midi (BaseModel):
    def __init__(self, header = None, tracks = []):
        self.header = header  # of type ByteChunk
        self.tracks = tracks # of type list of ByteChunk

    def add_track(self, track):
        self.tracks.append(track)
        return self

    