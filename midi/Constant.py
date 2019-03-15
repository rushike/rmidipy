class Constant:
    Mthd = (0x4d, 0x54, 0x68, 0x64)
    Mtrk = (0x4d, 0x54, 0x72, 0x6b)
    META_EVENT_END = (0x01, 0xff, 0x2f, 0x0)
    MAX = 1048576
    DTYPE = {'uint4': (0, 16), 'uint7': (0, 127), 'uint8' : (0, 256)}
    CHANNEL_EVENT = 'CHANNEL'
    META_EVENT = 'META'
    SYS_EVENT = 'SYS'

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
    #format = (id, "sub_event_name", "param_len", params..., "param_type", "common_range, -1", //if -1, highest_allowed_val_of_param..., -1, "mask")
    #If -1 in place of common range the following param len args are highesh values of parameters
    #If all within mask positive else masked negative
    meta_event_format = (
                            (0x00, "sequence_number", 2, "nmsb", "nlsb", "int", 256),
                            (0x01, "text_event", -1, "text", "str"),
                            (0x02, "copyright_notice", -1, "text", "str"),
                            (0x03, "track_name", -1, "text", "str"),
                            (0x04, "instrument_name", -1, "text", "str"),
                            (0x05, "lyrics", -1, "text", "str"),
                            (0x06, "marker", -1, "text", "str"),
                            (0x07, "cue_point", -1, "text", "str"),
                            (0x20, "midi_ch_prefix", 1, "channel", "int", 16),
							(0x21, "midi_port", 1, "port_no", "int", 16),
                            (0x2F, "end_of_track", 0, None, "None"),
                            (0x51, "set_tempo", 3, "musec_per_quat_note", "int", 8355712, 3),
                            (0x54, "smpte_offset", 5, "hr", "min", "sec", "fr", "subfr", "int", -1, 24, 60, 60, 30, 100),
                            (0x58, "time_sig", 4, "numer", "denom", "metro", "32nds", "int", 255),
                            (0x59, "key_sig", 2, "key", "scale", "int" ,-1, 14, 2, -1, 7),
                            (0x7F, "sequence_specifier", -1, "data", "any")
                        )
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
                    (0x10, "general_purpose_controller", 4, 0x50, 4),
                    (0x20, "LSB_for_controller", 32),
                    (0x40, "damper_pedal", 1),
                    (0x41, "portamento", 1),
                    (0x42, "sostenuto", 1),
                    (0x43, "soft_pedal", 1),
                    (0x44, "legato_footswitch", 1),
                    (0x45, "hold2", 1),
                    (0x46, "damper_pedal", 1),
                    (0x47, "sound_controller", 10),
                    (0x40, "damper_pedal", 1),
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

nhy = 909
