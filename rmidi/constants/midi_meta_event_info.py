import imp
import re
from .midi_event_info import MidiEventInfo

class MidiMetaEventInfo(MidiEventInfo):
    def __init__(self) -> None:
        super().__init__()
    
    @classmethod
    def ismetaevent(cls, eventbyte, subeventtype = 0):        
        return eventbyte == 0xff and subeventtype in cls.map[0xff]
    
    @classmethod
    def getinfo(cls, subeventbyte):
        return cls.map[0xff][subeventbyte] # returning midi meta event sub byte info

    @classmethod
    def getmask(cls, subeventbyte, index = 0):
        info = cls.getinfo(subeventbyte)
        if info["length"] < 1 : return info["mask"] # This are event with variable length (-1) or zero length end of track event
        return info["mask"][index] # fixed length meta event

    @classmethod
    def cast(cls, obj, dtype):
        print("cast : obj, dtype  : ", obj, dtype, type(obj))
        if dtype == 'str' and type(obj) == bytes: return obj.decode('utf-8') 
        elif dtype == 'str' : return str(obj)
        elif dtype == 'int' : return int(obj)

    map = {
        255: {
            0: {'dtype': 'int',
                'length': 2,
                'mask': (255, 255),
                'params': ('nmsb', 'nlsb'),
                'type_id': 0,
                'type_name': 'sequence_number',
                "default" : [0, 0]
                },
            1: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 1,
                'type_name': 'text_event',
                "default" : "Enter the Text"
                },
            2: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 2,
                'type_name': 'copyright_notice',
                "default" : "No Copyright"
                },
            3: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 3,
                'type_name': 'track_name',
                "default" : "Track 0"
                },
            4: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 4,
                'type_name': 'instrument_name',
                "default" : "Piano"
                },
            5: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 5,
                'type_name': 'lyrics',
                "default" : "LYRICS"
                },
            6: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 6,
                'type_name': 'marker',
                "default" : "*"
                },
            7: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 7,
                'type_name': 'cue_point',
                "default" : "-"
                },
            32: {'dtype': 'int',
                    'length': 1,
                    'mask': (15,),
                    'params': ('channel',),
                    'type_id': 32,
                    'type_name': 'midi_ch_prefix',
                    "default" : [0]
                    },
            33: {'dtype': 'int',
                    'length': 1,
                    'mask': (15,),
                    'params': ('port_no',),
                    'type_id': 33,
                    'type_name': 'midi_port',
                    "default" : [0]
                    },
            47: {'dtype': 'None',
                    'length': 0,
                    'mask': 127,
                    'params': None,
                    'type_id': 47,
                    'type_name': 'end_of_track',
                    "default" : None
                    },
            81: {'dtype': 'int',
                    'length': 3,
                    'mask': (127, 127, 127),
                    'params': ('musec_per_quat_note',
                            'musec_per_quat_note',
                            'musec_per_quat_note'),
                    'type_id': 81,
                    'type_name': 'set_tempo',
                    "default" : [0, 0, 0]
                    },
            84: {'dtype': 'int',
                    'length': 5,
                    'mask': (24, 60, 60, 30, 100),
                    'params': ('hr', 'min', 'sec', 'fr', 'subfr'),
                    'type_id': 84,
                    'type_name': 'smpte_offset',
                    "default" : [0, 0, 0, 0, 0]
                    },
            88: {'dtype': 'int',
                    'length': 4,
                    'mask': (255, 255, 255, 255),
                    'type_id': 88,
                    'type_name': 'time_sig',
                    "default" : [0, 0, 0, 0]
                    },
            89: {'dtype': 'int',
                    'length': 2,
                    'mask': (15, 1),
                    'params': ('key', 'scale'),
                    'type_id': 89,
                    'type_name': 'key_sig',
                    "default" : [0, 0]
                    },
            127: {'dtype': 'any',
                    'length': -1,
                    'mask': 127,
                    'params': 'text',
                    'type_id': 127,
                    'type_name': 'sequence_specifier',
                    "default" : [0,]
                    },
            'id': 255,
            'name': 'meta'
            }
        }