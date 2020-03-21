Mthd = (0x4d, 0x54, 0x68, 0x64)
Mtrk = (0x4d, 0x54, 0x72, 0x6b)
META_EVENT_END = (0x01, 0xff, 0x2f, 0x0)
MAX = 1048576
DTYPE = {'uint4': (0, 16), 'uint7': (0, 127), 'uint8' : (0, 256)}
CHANNEL_EVENT = 'CHANNEL'
sCHANNEL_EVENT = 'channel'
META_EVENT = 'META'
sMETA_EVENT = 'meta'
SYS_EVENT = 'SYS'
sSYS_EVENT = 'sys'

SCALE = ['c-major', 'c#-major', 'd-major', 'd#-major', 'e-major', 'f-major', 'f#-major', 
            'g-major', 'g#-major', 'a-major', 'a#-major', 'b-major', 
            'c-minor', 'c#-minor', 'd-minor', 'd#-minor', 'e-minor', 'f-minor', 'f#-minor', 
            'g-minor', 'g#-minor', 'a-minor', 'a#-minor', 'b-minor'
            ]

SCALE_OFFSET =  {'c-major' : 0, 'c#-major' : 1, 'd-major' : 2, 'd#-major' : 3,'e-major' : 4 ,'f-major' : 5, 'f#-major' : 6, 
                    'g-major' : 7, 'g#-major' : 8, 'a-major' : 9, 'a#-major' : 10, 'b-major' : 11, 
                    'c-minor' : 3, 'c#-minor' : 4, 'd-minor' : 5, 'd#-minor' : 6, 'e-minor' : 7, 'f-minor' : 8, 'f#-minor' : 9, 
                    'g-minor' : 10, 'g#-minor' : 11, 'a-minor' : 0, 'a#-minor' : 1, 'b-minor' : 2 
                    }


"""
KEY_SIG ENCODING
Everything according to circle of fifth
no. of #'s  0 -> 7
no. of b's  8 -> 15

SCALE_KEY_SIG : Contains string to integer mapping info
SCALE_KEY_SIG_DEFAULT : Contains string to integer mapping info, no. of #'s prefer over b, # naming system in presence of both flats(b) & sharp(#)
SCALE_KEY_SIG_REV : Contains integer to string mapping info
"""

SCALE_KEY_SIG_REV = {0 : ('c-major', 'a-minor'), 1 : ('g-major', 'e-minor'), 2 : ('d-major', 'b-minor'), 3 : ('a-major', 'f#-minor'), 4 : ('e-major', 'c#-minor'), 5 : ('b-major', 'g#-minor'), 6 : ('f#-major', 'd#-minor'), 7 : ('d#-major', 'a#-minor'),
                    8 : ('g-major', 'e-minor'), 9 : ('f-major', 'd-minor'), 10 : ('a#-major', 'g-minor'), 11 : ('d#-major', 'c-minor'), 12 : ('g#-major', 'f-minor'), 13 : ('c#-major', 'a#-minor'), 14 : ('f#-major', 'd#-minor'), 15 : ('b-major', 'g#-minor')
                    }

SCALE_KEY_SIG =  {'c-major' : (0, 8), 'c#-major' : (7, 13) , 'd-major' : (2, 8), 'd#-major' : (0, 11),'e-major' : (4, 8) ,'f-major' : (0, 9), 'f#-major' : (6, 14), 
                    'g-major' : (1, 8), 'g#-major' : (0, 12), 'a-major' : (3, 8), 'a#-major' : (0, 10), 'b-major' : (5, 15), 
                    'c-minor' : (0, 11), 'c#-minor' : (4, 8), 'd-minor' : (0, 9), 'd#-minor' : (6, 14) , 'e-minor' : (1, 8), 'f-minor' : (0, 12), 'f#-minor' : (3, 8),  
                    'g-minor' : (0, 10), 'g#-minor' : (5, 15) , 'a-minor' : (0, 8), 'a#-minor' : (7, 13) , 'b-minor' : (2, 8) 
                    }


SCALE_KEY_SIG_DEFAULT =  {'c-major' : 0, 'c#-major' : 7, 'd-major' : 2, 'd#-major' : 11,'e-major' : 4 ,'f-major' : 9, 'f#-major' : 6, 
                    'g-major' : 1, 'g#-major' : 12, 'a-major' : 3, 'a#-major' : 10, 'b-major' : 5, 
                    'c-minor' : 11, 'c#-minor' : 4, 'd-minor' : 9, 'd#-minor' : 6 , 'e-minor' : 1, 'f-minor' : 12, 'f#-minor' : 3, 
                    'g-minor' : 10, 'g#-minor' : 5 , 'a-minor' : 0, 'a#-minor' : 7 , 'b-minor' : 2 
                    }

ch_events = ("note_off", "note_on", "after_touch", "controller", "program_change", "channel_after_touch", "pitch_bend")

#format = (id, sub_event_name, param_len, params..., param_type)
ch_event_format = (
                    (0x8, "note_off", 2, "note_number", "velocity", "int"),
                    (0x9, "note_on", 2, "note_number", "velocity", "int"),
                    (0xA, "after_touch", 2, "note_number", "amount", "int"),
                    (0xB, "controller", 2, "controller_type", "value", "int"),                   
                    (0xC, "program_change", 1, "program_number", "int"),                   
                    (0xD, "channel_after_touch", 1, "amount", "int"),                   
                    (0xE, "pitch_bend", 2, "vlsb", "vmsb", "int")                  
                )

meta_events = ('sequence_number', 'text_event', 'copyright_notice', 'track_name', 
            'instrument_name', 'lyrics', 'marker', 'cue_point', 'midi_ch_prefix', 'midi_port', 
            'end_of_track', 'set_tempo', 'smpte_offset', 'time_sig', 'key_sig', 'sequence_specifier')
#format = (id, "sub_event_name", "param_len", params..., "param_type", "common_range, -1", //if -1, highest_allowed_val_of_param..., -1, "mask")
#If -1 in place of common range the following param len args are highesh values of parameters
#If all within mask positive else masked negative
meta_event_format = (
                        (0x00, "sequence_number", 2, "nmsb", "nlsb", "int", 255, 255),
                        (0x01, "text_event", -1, "text", "str"),
                        (0x02, "copyright_notice", -1, "text", "str"),
                        (0x03, "track_name", -1, "text", "str"),
                        (0x04, "instrument_name", -1, "text", "str"),
                        (0x05, "lyrics", -1, "text", "str"),
                        (0x06, "marker", -1, "text", "str"),
                        (0x07, "cue_point", -1, "text", "str"),
                        (0x20, "midi_ch_prefix", 1, "channel", "int", 15),
                        (0x21, "midi_port", 1, "port_no", "int", 15),
                        (0x2F, "end_of_track", 0, None, "None"),
                        (0x51, "set_tempo", 3, "musec_per_quat_note", "musec_per_quat_note", "musec_per_quat_note", "int", 127, 127, 127),
                        (0x54, "smpte_offset", 5, "hr", "min", "sec", "fr", "subfr", "int", 24, 60, 60, 30, 100),
                        (0x58, "time_sig", 4, "numer", "denom", "metro", "32nds", "int", 255, 255, 255, 255),
                        (0x59, "key_sig", 2, "key", "scale", "int" , 15, 1 ),
                        (0x7F, "sequence_specifier", -1, "data", "any")
                    )

sys_events = ("normal_sys_event", "authorization_sys_event")

sys_event_format = (
                        (0xF0, "normal_sys_event", -1, "data", "int", 128),
                        (0xF7, "authorization_sys_event", -1, "data", "int", 256),
                        
                    )

#controller format = (controller_value/id , "controller_type", "len_of_simmilar_extension")
controller = (
                (0x00, "blank_select", 1),
                (0x01, "modulation", 1),
                (0x02, "breath_controller", 1),
                (0x04, "foot_controller", 1),
                (0x05, "portamento_time", 1),
                (0x06, "data_entry", 1),#May be msb
                (0x07, "main_volume", 1),
                (0x08, "balance", 1),
                (0x0A, "pan", 1),
                (0x0B, "expression_controller", 1),
                (0x0C, "effect_control", 2),
                # (0x0D, "effect_control_2", 0),
                (0x10, "general_purpose_controller", 4),#, 0x50, 4),
                (0x20, "LSB_for_controller", 32),
                (0x40, "damper_pedal", 1),
                (0x41, "portamento", 1),
                (0x42, "sostenuto", 1),
                (0x43, "soft_pedal", 1),
                (0x44, "legato_footswitch", 1),
                (0x45, "hold", 1),
                # (0x46, "damper_pedal", 1),
                (0x46, "sound_controller", 10),
                # (0x40, "damper_pedal", 1),
                (0x50, "post_general_purpose_controller", 4),
                (0x54, "portamento_control", 1),
                (0x5B, "effects_depth", 5),
                (0x60, "data_increment", 1),
                (0x61, "data_decrement", 1),
                (0x62, "nonreg_param_num_lsb", 1),
                (0x63, "nonreg_param_num_msb", 1),
                (0x64, "reg_param_num_lsb", 1),
                (0x65, "reg_param_num_msb", 1),
                (0x79, "mode_messages", 7),
            )


ch_event_format = {
    8: {'id': 8,
        'length': 2,
        'mask': 127,
        'name': 'note_off',
        'params': ('note_number', 'velocity')},
    9: {'id': 9,
        'length': 2,
        'mask': 127,
        'name': 'note_on',
        'params': ('note_number', 'velocity')},
    10: {'id': 10,
        'length': 2,
        'mask': 127,
        'name': 'after_touch',
        'params': ('note_number', 'amount')},
    11: {0: {'cntrl_id': 0, 'cntrl_name': 'blank_select'},
        1: {'cntrl_id': 1, 'cntrl_name': 'modulation'},
        2: {'cntrl_id': 2, 'cntrl_name': 'breath_controller'},
        4: {'cntrl_id': 4, 'cntrl_name': 'foot_controller'},
        5: {'cntrl_id': 5, 'cntrl_name': 'portamento_time'},
        6: {'cntrl_id': 6, 'cntrl_name': 'data_entry'},
        7: {'cntrl_id': 7, 'cntrl_name': 'main_volume'},
        8: {'cntrl_id': 8, 'cntrl_name': 'balance'},
        10: {'cntrl_id': 10, 'cntrl_name': 'pan'},
        11: {'cntrl_id': 11, 'cntrl_name': 'expression_controller'},
        12: {'cntrl_id': 12, 'cntrl_name': 'effect_control_0'},
        13: {'cntrl_id': 13, 'cntrl_name': 'effect_control_1'},
        16: {'cntrl_id': 16, 'cntrl_name': 'general_purpose_controller_0'},
        17: {'cntrl_id': 17, 'cntrl_name': 'general_purpose_controller_1'},
        18: {'cntrl_id': 18, 'cntrl_name': 'general_purpose_controller_2'},
        19: {'cntrl_id': 19, 'cntrl_name': 'general_purpose_controller_3'},
        32: {'cntrl_id': 32, 'cntrl_name': 'LSB_for_controller_0'},
        33: {'cntrl_id': 33, 'cntrl_name': 'LSB_for_controller_1'},
        34: {'cntrl_id': 34, 'cntrl_name': 'LSB_for_controller_2'},
        35: {'cntrl_id': 35, 'cntrl_name': 'LSB_for_controller_3'},
        36: {'cntrl_id': 36, 'cntrl_name': 'LSB_for_controller_4'},
        37: {'cntrl_id': 37, 'cntrl_name': 'LSB_for_controller_5'},
        38: {'cntrl_id': 38, 'cntrl_name': 'LSB_for_controller_6'},
        39: {'cntrl_id': 39, 'cntrl_name': 'LSB_for_controller_7'},
        40: {'cntrl_id': 40, 'cntrl_name': 'LSB_for_controller_8'},
        41: {'cntrl_id': 41, 'cntrl_name': 'LSB_for_controller_9'},
        42: {'cntrl_id': 42, 'cntrl_name': 'LSB_for_controller_10'},
        43: {'cntrl_id': 43, 'cntrl_name': 'LSB_for_controller_11'},
        44: {'cntrl_id': 44, 'cntrl_name': 'LSB_for_controller_12'},
        45: {'cntrl_id': 45, 'cntrl_name': 'LSB_for_controller_13'},
        46: {'cntrl_id': 46, 'cntrl_name': 'LSB_for_controller_14'},
        47: {'cntrl_id': 47, 'cntrl_name': 'LSB_for_controller_15'},
        48: {'cntrl_id': 48, 'cntrl_name': 'LSB_for_controller_16'},
        49: {'cntrl_id': 49, 'cntrl_name': 'LSB_for_controller_17'},
        50: {'cntrl_id': 50, 'cntrl_name': 'LSB_for_controller_18'},
        51: {'cntrl_id': 51, 'cntrl_name': 'LSB_for_controller_19'},
        52: {'cntrl_id': 52, 'cntrl_name': 'LSB_for_controller_20'},
        53: {'cntrl_id': 53, 'cntrl_name': 'LSB_for_controller_21'},
        54: {'cntrl_id': 54, 'cntrl_name': 'LSB_for_controller_22'},
        55: {'cntrl_id': 55, 'cntrl_name': 'LSB_for_controller_23'},
        56: {'cntrl_id': 56, 'cntrl_name': 'LSB_for_controller_24'},
        57: {'cntrl_id': 57, 'cntrl_name': 'LSB_for_controller_25'},
        58: {'cntrl_id': 58, 'cntrl_name': 'LSB_for_controller_26'},
        59: {'cntrl_id': 59, 'cntrl_name': 'LSB_for_controller_27'},
        60: {'cntrl_id': 60, 'cntrl_name': 'LSB_for_controller_28'},
        61: {'cntrl_id': 61, 'cntrl_name': 'LSB_for_controller_29'},
        62: {'cntrl_id': 62, 'cntrl_name': 'LSB_for_controller_30'},
        63: {'cntrl_id': 63, 'cntrl_name': 'LSB_for_controller_31'},
        64: {'cntrl_id': 64, 'cntrl_name': 'damper_pedal'},
        65: {'cntrl_id': 65, 'cntrl_name': 'portamento'},
        66: {'cntrl_id': 66, 'cntrl_name': 'sostenuto'},
        67: {'cntrl_id': 67, 'cntrl_name': 'soft_pedal'},
        68: {'cntrl_id': 68, 'cntrl_name': 'legato_footswitch'},
        69: {'cntrl_id': 69, 'cntrl_name': 'hold'},
        70: {'cntrl_id': 70, 'cntrl_name': 'sound_controller_0'},
        71: {'cntrl_id': 71, 'cntrl_name': 'sound_controller_1'},
        72: {'cntrl_id': 72, 'cntrl_name': 'sound_controller_2'},
        73: {'cntrl_id': 73, 'cntrl_name': 'sound_controller_3'},
        74: {'cntrl_id': 74, 'cntrl_name': 'sound_controller_4'},
        75: {'cntrl_id': 75, 'cntrl_name': 'sound_controller_5'},
        76: {'cntrl_id': 76, 'cntrl_name': 'sound_controller_6'},
        77: {'cntrl_id': 77, 'cntrl_name': 'sound_controller_7'},
        78: {'cntrl_id': 78, 'cntrl_name': 'sound_controller_8'},
        79: {'cntrl_id': 79, 'cntrl_name': 'sound_controller_9'},
        80: {'cntrl_id': 80, 'cntrl_name': 'post_general_purpose_controller_0'},
        81: {'cntrl_id': 81, 'cntrl_name': 'post_general_purpose_controller_1'},
        82: {'cntrl_id': 82, 'cntrl_name': 'post_general_purpose_controller_2'},
        83: {'cntrl_id': 83, 'cntrl_name': 'post_general_purpose_controller_3'},
        84: {'cntrl_id': 84, 'cntrl_name': 'portamento_control'},
        91: {'cntrl_id': 91, 'cntrl_name': 'effects_depth_0'},
        92: {'cntrl_id': 92, 'cntrl_name': 'effects_depth_1'},
        93: {'cntrl_id': 93, 'cntrl_name': 'effects_depth_2'},
        94: {'cntrl_id': 94, 'cntrl_name': 'effects_depth_3'},
        95: {'cntrl_id': 95, 'cntrl_name': 'effects_depth_4'},
        96: {'cntrl_id': 96, 'cntrl_name': 'data_increment'},
        97: {'cntrl_id': 97, 'cntrl_name': 'data_decrement'},
        98: {'cntrl_id': 98, 'cntrl_name': 'nonreg_param_num_lsb'},
        99: {'cntrl_id': 99, 'cntrl_name': 'nonreg_param_num_msb'},
        100: {'cntrl_id': 100, 'cntrl_name': 'reg_param_num_lsb'},
        101: {'cntrl_id': 101, 'cntrl_name': 'reg_param_num_msb'},
        121: {'cntrl_id': 121, 'cntrl_name': 'mode_messages_0'},
        122: {'cntrl_id': 122, 'cntrl_name': 'mode_messages_1'},
        123: {'cntrl_id': 123, 'cntrl_name': 'mode_messages_2'},
        124: {'cntrl_id': 124, 'cntrl_name': 'mode_messages_3'},
        125: {'cntrl_id': 125, 'cntrl_name': 'mode_messages_4'},
        126: {'cntrl_id': 126, 'cntrl_name': 'mode_messages_5'},
        127: {'cntrl_id': 127, 'cntrl_name': 'mode_messages_6'},
        'id': 11,
        'length': 2,
        'mask': 127,
        'params': ['controller_type', 'value']},
    12: {'id': 12,
        'length': 1,
        'mask': 127,
        'name': 'program_change',
        'params': ('program_number',)},
    13: {'id': 13,
        'length': 1,
        'mask': 127,
        'name': 'channel_after_touch',
        'params': ('amount',)},
    14: {'id': 14,
        'length': 2,
        'mask': 127,
        'name': 'pitch_bend',
        'params': ('vlsb', 'vmsb')
        }
}



meta_event_format_dict = {
        0xFF: {
            0: {'dtype': 'int',
                'length': 2,
                'mask': (255, 255),
                'params': ('nmsb', 'nlsb'),
                'type_id': 0,
                'type_name': 'sequence_number'},
            1: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 1,
                'type_name': 'text_event'},
            2: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 2,
                'type_name': 'copyright_notice'},
            3: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 3,
                'type_name': 'track_name'},
            4: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 4,
                'type_name': 'instrument_name'},
            5: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 5,
                'type_name': 'lyrics'},
            6: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 6,
                'type_name': 'marker'},
            7: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 7,
                'type_name': 'cue_point'},
            32: {'dtype': 'int',
                    'length': 1,
                    'mask': (15,),
                    'params': ('channel',),
                    'type_id': 32,
                    'type_name': 'midi_ch_prefix'},
            33: {'dtype': 'int',
                    'length': 1,
                    'mask': (15,),
                    'params': ('port_no',),
                    'type_id': 33,
                    'type_name': 'midi_port'},
            47: {'dtype': 'None',
                    'length': 0,
                    'mask': 127,
                    'params': None,
                    'type_id': 47,
                    'type_name': 'end_of_track'},
            81: {'dtype': 'int',
                    'length': 3,
                    'mask': (127, 127, 127),
                    'params': ('musec_per_quat_note',
                            'musec_per_quat_note',
                            'musec_per_quat_note'),
                    'type_id': 81,
                    'type_name': 'set_tempo'},
            84: {'dtype': 'int',
                    'length': 5,
                    'mask': (24, 60, 60, 30, 100),
                    'params': ('hr', 'min', 'sec', 'fr', 'subfr'),
                    'type_id': 84,
                    'type_name': 'smpte_offset'},
            88: {'dtype': 'int',
                    'length': 4,
                    'mask': (255, 255, 255, 255),
                    'type_id': 88,
                    'type_name': 'time_sig'},
            0x59: {'dtype': 'int',
                    'length': 2,
                    'mask': (15, 1),
                    'params': ('key', 'scale'),
                    'type_id': 89,
                    'type_name': 'key_sig'},
            127: {'dtype': 'any',
                    'length': -1,
                    'mask': 127,
                    'params': 'text',
                    'type_id': 127,
                    'type_name': 'sequence_specifier'},
            'id': 255,
            'name': 'meta'
            }
}



sys_event_format_dict = {
    240: {
        "id": 240,
        "name": "normal_sys_event",
        "length": -1,
        "params": "data",
        "dtype": "int",
        "mask": 128
    },
    247: {
        "id": 247,
        "name": "authorization_sys_event",
        "length": -1,
        "params": "data",
        "dtype": "int",
        "mask": 256
    }
}