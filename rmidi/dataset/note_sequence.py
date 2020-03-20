from rmidi.dataset import config
from rmidi import mutils
from rmidi import MIDI
from rmidi import AbsoluteMidi
from rmidi.constant import converter
import numpy, json, pickle

class NoteSequence:
    def __init__(self, midi):
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
        

    @property
    def notes(self):
        pass

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

            pass
        pass
        return seq

    def to_rmidi(self):
        raise NotImplementedError("Method/Function is yet to be implemented")

    def __str__(self):
        seqlist = list(map( lambda trackitem : {f"track-{trackitem[0]}" : list(map(lambda eventitem: list(map(lambda item:  f"{item[0]} : {mutils.hexstr(item[1])}" if item[0] == 'data' else f"{item[0]} : {item[1]}", 
                        eventitem[1].items() )), trackitem[1].items()))} , self.seq.items()))
        return json.dumps(seqlist, indent=4, )
    
    def __repr__(self):
        return self.__str__()
