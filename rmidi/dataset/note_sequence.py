from rmidi.dataset import config
from rmidi import mutils
from rmidi import MIDI
from rmidi import AbsoluteMidi
from rmidi.constant import converter

import numpy, json, pickle
from collections.abc import Iterable
from collections import OrderedDict

class NoteSequence:
    def __init__(self, midi, oftype = "list", value = True):
        """Makes rmidi object or midi file transfer to magenta.NoteSequence like object
        
        Arguments:
            midi {rmidi | str --> filepath} -- can be rmidi object or path to midi file
        """
        if isinstance(midi, str): 
            if midi.endswith(('.mid', '.midi')):
                midi = abs(MIDI.parse_midi(midi))
            else : raise AttributeError(f"Attribute <midi> not a midi file path, path >> {midi}")
            # till here midi is translated to rmidi.MIDI or rmidi.AbsoluteMidi object
            self.seq = NoteSequence.parse(midi)
        if isinstance(midi, dict):
            self.seq = midi
        self.list = tuple(map(lambda track: tuple(map( lambda event: event[1] if value else event, track[1].items())), self.seq.items()))
        self.oftype = oftype
        self.value = value

    @property
    def notes(self):
        seq = {}
        for i, track in self.seq.items():
            seq[i] = {}
            for j, event in track.items():
                if event.get("type", "None") in ["note_on", "note_off"]:
                    seq[i][j] = self.seq[i][j]
        return NoteSequence(seq)

    def pitches(self, track, all = True):
        seq = {}
        for i, track_ in self.seq.items():
            if not all and track != i: continue
            seq[i] = []
            for j, event in track_.items():
                if event.get("type", "None") in ["note_on"]:
                    seq[i].append(self.seq[i][j]["pitch"])
        if not all: return seq[track]
        return seq
    
    def note_time(self, track = None, all = True):
        seq = {}
        for i, track_ in self.seq.items():
            if track and track != i: continue
            seq[i] = []
            for j, event in track_.items():
                if event.get("type", "None") in ["note_on"]:
                    seq[i].append((self.seq[i][j]["pitch"], self.seq[i][j]["time"]))
        if track: return seq[track]
        return seq
    
    def note_intervals(self, track = None, all = True):
        seq = {}
        for i, track_ in self.seq.items():
            if track and track != i: continue
            seq[i] = []
            for j, event in track_.items():
                if event.get("type", "None") in ["note_on"]:
                    seq[i].append((self.seq[i][j]["pitch"], self.seq[i][j]["duration"]))
        if isinstance(track, int) and track > -1 : return seq[track]
        return seq

    def order_by(self, attribute, reverse = False):
        """For now it support order by of only int or string attribute of event
        order by is intended to work for attributes 'time', 'duration', 'pitch', deltatime
        Arguments:
            attribute {str} -- attribute name
        """
        ordered_notes = self.pitches(0)
        seq = {}
        for i, track in ordered_notes.items():
            seq[i] = OrderedDict(sorted(track.items(), key = lambda x: x[1][attribute], reverse=reverse))
        return NoteSequence(seq)

    def to_abs_midi(self):
        tracks = len(self)
        midi = AbsoluteMidi.to_abs_midi(MIDI(format_type= 1, track_count = tracks, time_div=0x1e0, empty = True))
        for i, track in self.seq.items():
            midi.track(i).add_events_from_dict(track)
        return midi

    @classmethod
    def parse(cls, midi : AbsoluteMidi, notes = False):
        """[summary]
        
        Arguments:
            midi {AbsoluteMidi | MIDI} -- [description]
        
        Keyword Arguments:
            notes {bool} -- [description] (default: {False})
        """
        seq = {}
        for i, track in enumerate(midi):
            seq[i] = {}
            for j, event in enumerate(track):
                seq[i][j] = event.to_dict()
        return seq

    @classmethod
    def tostring(cls, seq):
        seqlist = list(map( lambda trackitem : {f"track-{trackitem[0]}" : list(map(lambda eventitem: 
                    list(map(lambda item:  f"{item[0]} : {mutils.hexstr(item[1])}" if item[0] == 'data' else f"{item[0]} : {item[1]}", 
                    eventitem[1].items() )), trackitem[1].items()))} , seq.items()))
        return json.dumps(seqlist, indent=4, )
    
    
    def length(self, track):
        return len(self[track])

    def track(self, track):
        return self.seq[track]
    
    def channel(self, track, channel_no):
        return list(filter(lambda event: event["channel"] == channel_no, self.seq.tracks[track]))
    
    def __getitem__(self, index):
        try:
            if not isinstance(index, Iterable) : return self.list[index]           
            track, event = index
            return self.list[track][event]
        except KeyError as K:
            raise KeyError(f"Index Out of Bound, getting event, track of the midi  {K}")

    def __len__(self):
        return len(self.seq)

    def __str__(self, seq = None):
        seq = seq if seq else self.seq
        seqlist = list(map( lambda trackitem : {f"track-{trackitem[0]}" : list(map(lambda eventitem: 
                    list(map(lambda item:  f"{item[0]} : {mutils.hexstr(item[1])}" if item[0] == 'data' else f"{item[0]} : {item[1]}", 
                    eventitem[1].items() )), trackitem[1].items()))} , seq.items()))
        return json.dumps(seqlist, indent=4, )
    
    def __repr__(self):
        return self.__str__()
