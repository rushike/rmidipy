
from rmidi.model.common.base import BaseModel


class MidiEvent (BaseModel):
    def __init__(self, block, deltatime, eventtype, content, **kwargs):
        self.block = block
        self.deltatime = deltatime
        self.eventtype = eventtype
        self.content = content
        self.kwargs = kwargs