import math
import numpy as np 
import os, os.path as pathmap
from Constant import Constant
from Track import Track
import mutils



class MIDI:
    def __init__(self, format_type = 0, track_count = 0, time_div = 0x1e0):
        # return super().__init__(*args, **kwargs)
        self.format_type = format_type
        self.track_count = track_count
        self.time_div = time_div
        self.tracks = [Track(self)] * track_count
        self.byte_list = bytearray()     

    def track(self, track_no):#Indexing from Zero
        if self.track_count < track_no : raise IndexError("Track no out of range")
        return self.tracks[track_no]
    def to_byte_array(self):
        byte_list = bytearray()
        byte_list.append(Constant.Mthd)
        byte_list.append(mutils.to_fix_length(self.format_type, 2, 8))
        byte_list.append(mutils.to_fix_length(self.track_count, 2, 8))
        byte_list.append(mutils.to_fix_length(self.time_div, 2, 8))
        for trk in self.tracks:
            byte_list.append(trk.to_byte_array())
        le = len(byte_list) - 10
        byte_list.insert(4, mutils.to_fix_length(le, 4, 8))
        return byte_list
    
    def create_file(self, file_name, loc = pathmap.abspath(os.curdir)):
        with open(loc + "/" + file_name, "wb+") as f:
            f.write(self.to_byte_array())



