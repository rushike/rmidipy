import math, random, copy
import numpy as np 
import os, os.path as pathmap
from rmidi import mutils
import itertools
from rmidi.constant import converter
import rmidi as constant
from rmidi.constant import X

numpy = np

WRAP_DATA = 0x7f
WRAP_BITS = 7

def ch_event_id(id, no) :
    return ((id & 0xf) << 4) + (no & 0xf)

def metype(typ):
    return typ & 0xff

def to_var_length(k):
    if k > 127:
        leng = length(k) // WRAP_BITS + 1
        var = bytearray(leng)
        var[-1] = k & WRAP_DATA
        k >>= WRAP_BITS
        for i in range(leng - 2, -1, -1):
            var[i] = (k & WRAP_DATA) + WRAP_DATA + 1
            k >>= WRAP_BITS
        return var
    else:
        return bytearray((k,))     

def to_fix_length(k, leng, bits):
    fix = bytearray(leng)
    wrapper = (1 << bits) - 1
    if k > 255 and k > -1:
        fix[-1] = k & wrapper
        k >>= bits
        for i in range(leng - 2, -1, -1):
            fix[i] = (k & wrapper) + wrapper + 1
            k >>= bits
    elif k > -1 :
        fix[-1] = k & 0xff
    return fix

def up(n_b, base = 2):
    return base ** int(math.log2(n_b) / math.log2(base) + 1)
    
def split(n, t, block_size = None): #Splits 'n' integer in t integer of bits bit(n)/t
    n_b = length(n)
    sbit = up(n_b) // t if not block_size else block_size
    WRAPPER = 2 ** sbit - 1
    k = n
    li = []
    while k:
        li.append(k & WRAPPER)
        k >>= sbit
    le = t - len(li)
    for _ in range(le):
        li.append(0)
    li.reverse()
    return li


def merge(a, b, *nums, block_size = 16):#Merge the numbers in order
    WRAPPER = (1 << block_size) - 1
    num = ((a & WRAPPER) << block_size) + (b & WRAPPER)
    for v in nums:
        num = (num << block_size) + (v & WRAPPER)
    return num


def length(k):
    """Finds length of k in bits
    
    Arguments:
        k {int} -- Integer number
    """
    return int(math.log2(k) + 1)
def find_location(text, listt):
    try:
        return next((i, j) 
            for i, t in enumerate(listt)
            for j, v in enumerate(t)
            if v == text)
    except StopIteration:
        return None

class constant:
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


class MIDI:
    def __init__(self,  format_type = 0, track_count = 0, time_div = 0x1e0, empty = False, filename = None, ):
        self.pipe = {}
        self.filename = filename
        self.format_type = format_type
        self.track_count = track_count
        self.time_div = time_div
        self.tracks = [MIDI.Track(self, empty= empty) for _ in range(track_count)]
        self.byte_list = bytearray()     

    def track(self, track_no):#Indexing from Zero
        if self.track_count < track_no : raise IndexError("Track no out of range")
        return self.tracks[track_no]
    def set_time_div(self, val, inbpm = True): 
        """val acts as actual bpm value if inbpm is True, 
         or as no ticks per seconds count if inbpm is False
         It actually sets ticks resolution
        Arguments:
            self {MIDI} -- [description]
            val {int} 
        Keyword Arguments:
            inbpm {bool} -- [description] (default: {True})
        """
        val = (val * .5e6 ) // 7200 if inbpm else val 
        self.pipe['ntime_div']  = val
        self.time_div = val

    def to_byte_array(self):
        byte_list = self.__midiheaderbytes()

        for trk in self.tracks:
            byte_list.extend(trk.to_byte_array())
        return byte_list
    
    def create_file(self, file_name, loc = pathmap.abspath(os.curdir)):
        with open(loc + "/" + file_name + ".mid", "wb+") as f:
            df = self.to_byte_array()

            f.write(df)

    @classmethod
    def parse_midi(cls, filename):
        with open(filename, 'rb') as f:
            content = f.read()
            return MIDI.parse(content)
        return None

    @classmethod
    def parse(cls, content):
        try : 
            vmthd = content[:4]
            vlength = mutils.toint(content[4:8])
            vformat_type = mutils.toint(content[8:10])
            vtrack_count = mutils.toint(content[10:12])
            vtime_div = mutils.toint(content[12:14])

            mid = cls(vformat_type, vtrack_count, vtime_div, empty = True)
            utape = 14
            for i, t in enumerate(mid.tracks):
                vmtrk = content[utape: utape + 4]
                lentr = mutils.toint(content[utape + 4: utape + 8])
                # print(f"trk : {i}, utape : {utape}, lentr : {lentr}, content leng : {mutils.hexstr(content[utape : utape + 8])}")
                utape += (lentr + 8)
                trkip = content[utape - lentr : utape]

                leny = len(trkip)
                if leny == 0: break
                trk_elist = []
                to, fr = 0, 0 #Start state
                tape = -1 #Start at far left

                vbuf = bytearray()
                del_time = 0
                kparams = {}
                # print('trk :\n', mutils.hexstr(trkip, leng= 16, group=2, numlen= 2))
                # hex_string = "".join("%02x" % b for b in content)
                # print("E--> ", hex_string)
                # print(trkip)
                while True:
                    if tape > leny: 
                        # print(f"tape : {tape},  leny : {leny} , rklist : {mutils.hexstr(trkip[:], leng = 16)}")
                        raise ValueError("File has sys event, not supported by us : rmidi")

                    tape += 1
                    # print('tape ---> ', tape)
                    # if tape < leny : print('state =: ', to , ', tape ---> :', hex(tape), ',  i/p : ', hex(trkip[tape]))
                    if to == 0: #Init State, Deltatime Detection
                        vbuf.append(trkip[tape])
                        if trkip[tape] < 0x80:
                            del_time = mutils.vartoint(vbuf)
                            vbuf = bytearray()
                            to = 1

                    elif to == 1: #Event Detection
                        # print('In event Detection L : ')
                        if 0x80 <= trkip[tape] < 0xF0: to = 2 #Channel Event
                        elif trkip[tape] == 0xFF: to = 7 #Meta Event 
                        elif trkip[tape] == 0xF0 or trkip[tape] == 0xF7 : to = 4
                        elif 'fromevent' in kparams:
                            if kparams['fromevent'] == 'Channel':
                                tape -= 1
                                to = 5
                            else : raise ValueError('kparams wrongly set , attr - fromevent is ' + kparams['fromevent']) 
                        else : raise Exception('Error in Event detection phase : no event matched ... event id : ' + hex(trkip[tape]))
                    
                    elif to == 2: #Channel Event
                        tape -= 1
                        ev = mutils.numin(trkip[tape], 4, 4)
                        ind = find_location(ev, constant.ch_event_format)
                        if ind:
                            evt_info = constant.ch_event_format[ind[0]]
                            kparams['event_id'] = trkip[tape]
                            kparams['len'] = evt_info[2]
                            to = 5
                            pass
                        else : raise Exception("Can't parse the file\nChannel Event not in parsers list\nChannel Event ID: " + hex(trkip[tape]))
                        fr = 2
                        
                    elif to == 3: #Meta Event
                            if 'mlength' in kparams:
                                # print("le = ", hex(kparams.get('le')), ", ip len : ", hex(kparams.get('mlength')))
                                if kparams.get('le') == 0:
                                    trk_elist.append(MIDI.Track.Event.MetaEvent(del_time, stype, params= ()))
                                    break
                                elif kparams.get('le') == kparams.get('mlength') or kparams.get('le') == -1:
                                    tape += kparams.get('mlength')
                                    params = trkip[tape - le: tape]
                                    trk_elist.append(MIDI.Track.Event.MetaEvent(del_time, stype, params= params))
                                    tape -= 1
                                else: raise ValueError("Event length from file cant match with list avail.")
                            else: raise Exception('kparams errors... mlength not in kparams')

                            kparams['fromevent'] = 'Meta'
                            to = 0
                            
                
                    elif to == 4: #Sys Event
                        to = 6
                        kparams['sys_event_id'] = trkip[tape] 
                        kparams['fromevent'] = 'sys'
                        # print(f"Sys event on tape : {tape}")
                        pass
                    elif to == 5: #Sub Channel Event
                        tape += kparams.get('len') 
                        params = trkip[tape - kparams.get('len') : tape]
                        tape -= 1
                        # print('params : ',mutils.hexstr(params))
                        trk_elist.append(MIDI.Track.Event.ChannelEvent(del_time, kparams.get('event_id'), params= params))
                        kparams['fromevent'] = 'Channel'
                        to = 0

                    elif to == 6: #Var length calculator
                        vbuf.append(trkip[tape])
                        if trkip[tape] < 0x80:
                            kparams['mlength'] = mutils.vartoint(vbuf)
                            vbuf = bytearray()
                            if 'fromevent' in kparams:
                                if kparams['fromevent'] == 'sys':
                                    # print(f"sys event on tape : {tape} with mlength : {kparams['mlength']}")
                                    to = 8
                                    continue
                            to = 3
                        pass
                    elif to == 7: #Meta sub event
                        ind = find_location(trkip[tape], constant.meta_event_format)
                        if ind:
                            evt_info = constant.meta_event_format[ind[0]]
                            stype = evt_info[0]
                            le = evt_info[2]
                            kparams['le'] = le
                            kparams['stype'] = stype
                            to = 6
                        else : raise Exception(str(e) + "\nCan't parse the file\nMeta Event Subtype not in parsers list\nMeta Event Subtype ID: " + hex(trkip[tape]))
                    elif to == 8:
                        if 'mlength' in kparams:
                            tape += kparams.get('mlength')
                            params = trkip[tape - kparams.get('mlength') : tape]
                            trk_elist.append(MIDI.Track.Event.SysEvent(del_time, kparams.get('sys_event_id'), params))
                            # print(f"Appended Sys Event Successfully.")
                        to == 0


                t.__reinit__(id, len(trk_elist), trk_elist, mid)
        except Exception as e:
            raise Exception('Something not alright : rimidi --> ' + str(e))
        # print(mid)
        return mid
    def decompress(self):
        if self.filename is not None:
            return MIDI.parse_midi(self.filename)

    def compress(self, filename = 'default'):
        bytelist = self.__midiheaderbytes()
        # print("H : ", mutils.hexstr(bytelist))
        ch_active = False
        for t in self.tracks:
            bytelist.extend(constant.Mtrk)
            start = len(bytelist)
            eventbuff = bytearray()
            for e in t.trk_event:
                eventbuff = e.to_byte_array()
                if e.etype == constant.CHANNEL_EVENT:
                    if ch_active == e.event_id: eventbuff.remove(e.event_id)
                    ch_active = e.event_id
                    pass
                else : ch_active = False
                bytelist.extend(eventbuff)
            le = mutils.to_fix_length(len(bytelist) - start, 4, 8)
            for i in range(start, start + 4):
                bytelist.insert(i, le[i - start - 4])
        with open(filename + '.mid','wb+') as f:
            f.write(bytelist)
        return bytelist


    """
    Function for all tracks, 
    """

    def transpose_to(self, scale, s_type = 0, new = False):
        self_copy = copy.deepcopy(self)
        for t in self_copy.tracks:
            t.transpose_to(scale, s_type)
        return self_copy

    def change_scale(self, scale, s_type = 0, new = False):
        self_copy = copy.deepcopy(self)
        for t in self_copy.tracks:
            t.change_scale(scale)
        return self_copy

    def note_frequencies(self):
        freq_count = numpy.zeros((self.track_count, 256))
        for t in range(self.track_count):
            freq_count[t] = self.tracks[t].note_frequencies()
        return freq_count

    def __midiheaderbytes(self):
        byte_list = bytearray()
        byte_list.extend(constant.Mthd)
        byte_list.extend(mutils.to_fix_length(6, 4, 8))
        byte_list.extend(mutils.to_fix_length(self.format_type, 2, 8))
        byte_list.extend(mutils.to_fix_length(self.track_count, 2, 8))
        byte_list.extend(mutils.to_fix_length(self.time_div, 2, 8))
        return byte_list
    
    def __refresh__(self):
        for t in self.tracks:
            pass
    
    def __abs__(self):
        from rmidi import AbsoluteMidi
        return AbsoluteMidi.to_abs_midi(self)
    
    def __len__(self):
        return self.track_count

    def __getitem__(self, index):
        """Makes objbect iterable, like array<br>
        AbsoluteMidi can behave as 3D array, at 3rd level it will return event.attribute
        
        index:
            type : int | tuple
            int --> it represent track, method will return track
            tuple --> max length : 3 (track, event, attribute)

        Arguments:
            index {int | tuple} -- int or tuple, int represent track, see index definition above
        """
        if isinstance(index, int):
            return self.track(index)
        if isinstance(index, tuple):
            if len(index) == 1:
                return self.track(index)
            elif len(index) == 2:
                return self.track(index[0]).note(index[1])
            raise IndexError(f"Tuple length > 2, len : {len(index)}, index : {index}")
        raise IndexError(f"Index might not be tuple or int")

    def __repr__(self):
        st = ""
        mstr = '______________________________________________________________________________________________________________________________ . . . \n'
        mstr += '| Absolute Time   |  Duration       |  Delta Time |  ETYPE     |   Event ID | META  | LENGTH     | DATA \n' #% (e.abstime, e.elength, hex(e.delta_time), e.etype, hex(e.event_id), mhxmet, hex(e.leng()),  mutils.hexstr(e.data, group= 2))
        mstr += '|______________________________________________________________________________________________________________________________ . . . \n'
        st += mstr        
        for t in self.tracks:
            st = st + t.__repr__() # + "\n" 
            st += '******************************************************************************************************************************'
        return st

    class Track:
        def __init__(self, midi, empty = False):
            self.id = 0
            self.length = 0
            self.trk_event = []
            self.midi_ = midi
            # self.track_m = self
            if empty : return
            self.trk_event.append(MIDI.Track.Event.MetaEvent(0, 0x58,(0x4, 0x2, 0x18, 0x8))) #Meta Event : Time Signature
            self.trk_event.append(MIDI.Track.Event.MetaEvent(0, 0x59, (0x0, 0x0))) #Meta Event : Key Signature
            self.trk_event.append(MIDI.Track.Event.MetaEvent(0, 0x51, (0x7, 0xa1, 0x20)))
            self.trk_event.append(MIDI.Track.Event.ChannelEvent(0, 0xb, 0x0, (0x79, 0))) #Channel Event : Controller  Blank Select
            self.trk_event.append(MIDI.Track.Event.ChannelEvent(0, 0xc, 0, (0x0,))) #Channel Event : Program Change Event
            self.trk_event.append(MIDI.Track.Event.ChannelEvent(0, 0xb, 0, (0x7, 0x64))) #Channel Event : Controller  Main Volume
            self.trk_event.append(MIDI.Track.Event.ChannelEvent(0, 0xb, 0, (0x0a, 0x40))) #Channel Event : Controller  Pan
            self.trk_event.append(MIDI.Track.Event.ChannelEvent(0, 0xb, 0, (0x5b, 0x00)))#/Channel Event : Controller  External Effects Depth
            self.trk_event.append(MIDI.Track.Event.ChannelEvent(0, 0xb, 0, (0x5d, 0x00))) #Channel Event : Controller  formerly Chorus Depth
            self.trk_event.append(MIDI.Track.Event.MetaEvent(0, 0x04, params="Piano")) # Intrument name
            self.trk_event.append(MIDI.Track.Event.MetaEvent(0, 0x21,(0x00,))) # Meta Event : Midi Port/ Should be prior to anyone
            
            self.trk_event.append(MIDI.Track.Event.MetaEvent(0, 0x2f, None)) #Meta Event : End of Track
        
        def __reinit__(self, id, length, trk_event, midi_):
            self.id = id
            self.length = length
            trk_event_copy = copy.deepcopy(trk_event)
            # print("Trakc : ... ", trk_event)
            # print("Track Length : ", len(trk_event))
            self.trk_event = [v for v in trk_event_copy]
            # print("Trak : ... ", self.trk_event)
            self.midi_ = midi_

        def _add_event(self, evt):
            end = self.trk_event.pop()
            self.trk_event.append(evt)
            self.trk_event.append(end)
            return None

           

        def set_tempo(self, time, tempo):
            tmp = ((500000 * 120) // tempo)
            self.add_event(0, 'set_tempo', tempo = tmp)

        def tempo(self):
            return mutils.toint(self.get_event('set_tempo', depth = 1)[0].data, 8)

        def transpose_to(self, scale, s_type = 0, offset = -256, new = False):
            self_copy = copy.deepcopy(self) if new else self
            if offset != -256: pass

            elif type(scale) == int and -7 < scale < 7 : 
                scale_id, s_type = self.get_scale(string= False)
                scale = constant.SCALE[scale_id + s_type & 12]
            elif scale in constant.SCALE:
                 scale_id, s_type = self.get_scale()
                 offset = (constant.SCALE_OFFSET[scale_id] - constant.SCALE_OFFSET[scale])  
            else : raise AttributeError("Scale not defined. ")
            
            for e in self_copy.trk_event:
                if e.is_note_on_off_event():
                    e.data[0] -= offset
            return self_copy

        def transpose(self, tval):
            arr = self.notes()
            return [(arr[0], arr[1] + tval, arr[2]) for v in arr]

        def change_scale(self, scale, octave = 1, new = False):
            """Change the scale of midi track,  
            Assumes the c-major has no flats instead no sharps;  key sig event will    | 0xFF      |  0x59      |         0x00            |            0x01            |
                                                                                        meta marker  key-sig       no of sharps or flats      flat or sharp indicator  
            
            Arguments:
                scale {string} -- scale name in sharp notation format, like c-major, a#-minor

            
            Keyword Arguments:
                new {bool} -- if change scale on new duplicated track (default: {False})
                ocatave{int} -- relative integer indicating to tranfer or scale change in back or ahead octave {default: {1}}
            """
            self_copy = copy.deepcopy(self) if new else self
            if scale in constant.SCALE_OFFSET:
                scale_id, s_type = self.get_scale()

                key_sig_event = self.get_event('key_sig', new = False, depth = 1)[0]
                key_sig = [(constant.SCALE_KEY_SIG[scale][0] & 7) ,  mutils.invert(constant.SCALE_KEY_SIG[scale][1] & 7, 8, True)]
                key_sig = [key_sig[1], 1] if key_sig[0] == 0 else [key_sig[0], 0] # convert  the key sig tuple to (data, type) tuple as in midi format
                key_sig_event.set_date_params(key_sig)

                transpose_int = (constant.SCALE_OFFSET[scale_id] - constant.SCALE_OFFSET[scale]) - (octave - 1) * 12
                self.transpose_to(0, offset= transpose_int)
                return key_sig_event
            return None

        def get_scale(self, string = True, sharps = False):
            """Finds the scale, or pattern in which track is. Can only find major, minor scale for now 
            
            Keyword Arguments:
                string {bool} -- True if wants string - representation of scale(SCALE NAME) (default: {True})
                ifmajor {int} -- [description] (default: {0})
            
            Raises:
                NotImplementedError: [description]
            
            Returns:
                [type] -- [description]
            """
            # event_info = mutils.find_in_nested_dict(constant.meta_event_format_dict, 'key_sig')
            event_info = constant.meta_event_format_dict[0xFF][0x59] # 0x59 <---> key_sig
            sharps = 1 if sharps else 0
            for e in self.trk_event:
                # e =  Event()
                # if e.is_meta_event() : print(e)
                if e.meta_event_type == 0x59: #  0x59 <---> key_sig, key signature event
                    key, scale = mutils.magnitude(e.data[0], 8), e.data[1]
                    if string: return constant.SCALE_KEY_SIG_REV[key | ((sharps & 1) | 8)][sharps], scale    
                    return key | ((scale & 1) | 8), scale
                    # raise NotImplementedError("Implement the get_scale to use it.") 
            if string: return 'c-major', 0
            return 0, 0
        def get_event(self, event, depth = 10000, new = True):
            res = []
            ind1 = find_location(event, constant.ch_event_format)
            dep = 0
            if ind1:
                id_ = constant.ch_event_format[ind1[0]][0]
                for e in self.trk_event:
                    if e.event_id == id_: 
                        # res.append(copy.deepcopy(e))
                        if new : res.append(copy.deepcopy(e))
                        else : res.append(e)
                    dep += 1
                    if dep > depth: break
                return res            
            ind2 = find_location(event, constant.meta_event_format)
            dep = 0
            if ind2:
                id_ = constant.meta_event_format[ind2[0]][0]
                event_info = constant.meta_event_format[0xFF][id_]
                # event_info = event_info['0xFF'][mutils.hex2(id_)]
                for e in self.trk_event:
                    if e.meta_event_type == id_: 
                        if new : res.append(copy.deepcopy(e))
                        else : res.append(e)
                        dep += 1
                        if dep > depth: break
                if id_ in {0x4} and len(res) == 0: 
                    ne = MIDI.Track.Event.MetaEvent(0, id_, event_info['default'])
                    return [ne]
                return res

            # ind = ind1 if not ind1  else ind2 if not ind2  else None
            # print("ind : From get_event --  ", ind)
            # if not ind:
            #     print("id_ : From get_event -- ", id_)
                
        def add_event(self, time, event, **kparams):#Can't add key sig event for now
            if 'delta' in kparams:
                pass
            else:
                if type(event) == str:
                    #Adding channel event
                    ind = find_location(event, constant.ch_event_format)
                    # if event in itertools.chain(*constant.ch_event_format):
                    if ind:
                        evt_info = constant.ch_event_format[ind[0]]
                        ch_no = kparams.get('channel_no') if 'channel_no' in kparams else 0
                        event_id = (evt_info[0] << 4) | (ch_no & 7)
                        if 'params' in kparams:
                            params = kparams.get('params')
                            if len(params) != evt_info[2]: raise ValueError("params length not matched to actual parameter")
                            pass
                        else:
                            params = [0] * evt_info[2]
                            for i in range(3, 3 + evt_info[2]):
                                if  evt_info[i] in kparams:
                                    params[i - 3] = kparams.get(evt_info[i])
                                    pass
                                else: raise ValueError("Attribute " + evt_info[i] + " not in parameters")
                        self._add_event(MIDI.Track.Event(delta_time= self.delta_time(time), etype= constant.CHANNEL_EVENT, event_id= event_id, data=bytearray(params)))
                        return True
                    #Adding meta event    
                    ind = find_location(event, constant.meta_event_format)
                    if ind :
                        evt_info = constant.meta_event_format[ind[0]]
                        event_id = 0xff
                        meta_event_type = evt_info[0]
                        if event == 'set_tempo':
                            a, b, c = split(kparams.get('tempo'), 3, 8)
                            self._add_event(MIDI.Track.Event(delta_time=self.delta_time(time), etype= constant.META_EVENT, event_id= event_id, meta_event_type= meta_event_type, data= bytearray((a, b, c))))
                            return
                        if evt_info[2] == -1:
                            if 'text' in kparams:
                                if type(kparams.get('text')) == str:
                                    params = kparams.get('text').encode('utf-8')
                                else :raise ValueError("Event : " + event + " text attribute is nor string")
                            elif 'data' in kparams:
                                if type(kparams.get('data')) == str:
                                    params = kparams.get('data').encode('utf-8')
                                else :raise ValueError("Event : " + event + " text attribute is nor string")
                        elif evt_info[2] == 0: self.trk_event.append(MIDI.Track.Event.MetaEvent(0, 0x2f, None)) #Meta Event : End of Track
                        else :
                            if evt_info[3+ evt_info[2]] == -1:
                                if 'key_sig' in kparams:
                                    return
                                maxr = [evt_info[i] for i in range(4 + evt_info[2], 4 + 2 * evt_info[2])]
                            else : maxr = [evt_info[3+ evt_info[2]]] * evt_info[2]
                            # print(maxr)
                            for i in range(3, 3 + evt_info[2]):
                                params = [0] * evt_info[2]
                                if evt_info[i] in kparams:
                                    params[i - 3] = kparams.get(evt_info[i]) % maxr[i]
                                    pass
                                else : raise ValueError("Attribute " + evt_info[i] + " not in parameters")

                        self._add_event(MIDI.Track.Event(delta_time= self.delta_time(time), etype= constant.META_EVENT, event_id= event_id, meta_event_type= meta_event_type, data=bytearray(params)))

                        pass
                    if event in itertools.chain(*constant.ch_event_format):
                        pass
                else:
                    raise ValueError("Inappropiate Arhument Value, event not of type string")


            return None
        def push_note(self, note_length, note_val, channel_no = 0, intensity = 0x50):
            """Pushes the note on self track, over midi object
            
            Arguments:
                note_length {int} -- tradition note length, whole(1), half(2), quater(4) and so on
                note_val {int} -- Corrseponding note value, related to midi encoding
            
            Keyword Arguments:
                channel_no {int} -- midi channel , necessity for channel (default: {0})
                intensity {hexadecimal} -- loudness, volume, or how hard the note is hit (default: {0x50})
            """
            end = self.trk_event.pop()
            self.trk_event.append(MIDI.Track.Event.ChannelEvent(self.delta_time(note_length), 0x9, channel_no, (note_val, intensity)))
            self.trk_event.append(end)


        def close_note(self, note_length, note_val, channel_no, intensity = 0):
            """Pushes the note on self track, over midi object
            
            Arguments:
                note_length {int} -- tradition note length, whole(1), half(2), quater(4) and so on
                note_val {int} -- Corrseponding note value, related to midi encoding
            
            Keyword Arguments:
                channel_no {int} -- midi channel , necessity for channel (default: {0})
                intensity {hexadecimal} -- loudness, volume, or how hard the note is hit (default: {0x50})
            """
            end = self.trk_event.pop()
            self.trk_event.append(MIDI.Track.Event.ChannelEvent(self.delta_time(note_length), 0x8, channel_no, (note_val, 0x30)))
            self.trk_event.append(end)
            
        def end_track(self):
            self.trk_event.append(MIDI.Track.Event.MetaEvent(0, 0x2f, None))
        
        def delta_time(self, note_length):#Computes the delta time from tradition note duration, full, half, quater 
            """ Computes the delta time from tradition note duration, full, half, quater 
            Assumes every midi file of 4 / 4 key sig for now 
            
            Arguments:
                note_length {int} -- tradition note duration, full(1), half(2), quater(4)
            Returns:
                [int] -- delta_time
            """
            if not note_length: return 0
            return (self.midi_.time_div * 4) // note_length
        
        def leng(self):#Returns length in bytes
            szn = 0
            for e in self.trk_event:
                szn += e.leng()
            return szn
        
        def to_byte_array(self):
            byte_list = bytearray()
            byte_list.extend(constant.Mtrk)
            # byte_list.append([0] * 4)
            for e in self.trk_event:
                byte_list.extend(e.to_byte_array())
            le = mutils.to_fix_length(self.leng(), 4, 8)
            for i in range(4, 8):
                byte_list.insert(i, le[i - 4])
            return byte_list

        def note_frequencies(self):
            freq_count = numpy.zeros(256) #index represent midi note
            for e in self.trk_event:
                # e = Event()
                if e.is_note_off_event():
                    freq_count[e.data[0]] += 1 #incerementin note count of data[0]
            return freq_count

        def min_note(self):
            fre = numpy.trim_zeros(self.note_frequencies())
            return fre[0]
            
        def notes(self, abs = True, eventtype = None):
            dictn = {}
            res = []
            res_bpm = [(0, 500000),]
            timekeeper = 0 #in microsecods
            for t in self.trk_event:
                timekeeper += (t.delta_time / self.midi_.time_div * res_bpm[-1][1])
                if 0x80 <= t.event_id < 0xa0:   
                    eventid = t.event_id >> 4
                    noteval = t.data[0]
                    velocity = t.data[1] 
                    to = 0
                    #DFA Inside
                    if to == 0:#Delta time == 0
                        to = 1 
                    if to == 1: #check if closing the node
                        if (eventid  & 0xf == 8) or velocity == 0: to = 3
                        else : to = 2
                    if to == 2: # push the current time
                        dictn[noteval] = timekeeper
                        to = -1
                    if to == 3: # assign the duration
                        duration = timekeeper - dictn[noteval]
                        to = 4
                    if to == 4: # store in res
                        res.append(((timekeeper - duration)/1e6, noteval, duration/1e6))
                        
                elif t.event_id == 0xff and t.meta_event_type == 0x51:
                    microsecods = t.get_data()
                    if (timekeeper, microsecods) not in res_bpm: res_bpm += [(timekeeper, microsecods)]
            return {'note_series' : res, 'bpm_change' : res_bpm}  
        
        def note(self, index):
            if isinstance(index, int):
                return self.trk_event[index]
            raise IndexError(f"Indexes must be of type int, got of type {type(index)}, index {index}")

        def __refresh__(self):
            for t in self.trk_event:
                pass

        def __repr__(self):
            st = ""
            for e in self.trk_event:
                st = st +  e.__repr__() # + "\n"
            return st
        
        def __getitem__(self, index):
            if isinstance(index, int):
                return self.note(index)
            raise IndexError(f"Indexes must be of type int, got of type {type(index)}, index {index}")


        class Event :
            
            def __init__(self, delta_time = 0, etype = None, event_id = None, meta_event_type = None, length = 0, data = bytearray()):
                self.delta_time = delta_time # int encoded representing time elapsed from previous event
                self.etype = etype # str representation for event type, CHANNEL, META, SYS
                self.event_id = event_id # represent event type code, like 0xFF for Meta Event, 0x8_ - 0xE_ for channel, 0x and 0xF0 , 0xF7 for Sys Event 
                self.meta_event_type = meta_event_type # represent Meta Sub event code
                self.length = length # represent length of event, total event length including delta time in bytes
                self.data = data # stores event data after event id, for Meta dta after Meta Sub Event length in bytes 
                self.bytes = bytearray() # strores bytes representation of entire event
                self.abstime = 0 # Only use if Object is of type Absolute Midi, absolute time passed from start in seconds
                self.elength = 0 # Only use if Object is of type Absolute Midi, total event length in seconds
                # self.to_byte_array()

            def set_date_params(self, params):
                self.data = bytearray(params)

            def scale_delta_time(self, factor):
                self.delta_time = self.delta_time * factor

            def get_data(self, asnum = True, msb = True):
                return mutils.toint(self.data, 8)
            
            def is_channel_event(self):
                return self.etype == constant.CHANNEL_EVENT

            def is_meta_event(self):
                return self.etype == constant.META_EVENT

            def is_sys_event(self):
                return self.etype == constant.SYS_EVENT
            def is_note_on_off_event(self):
                return 0x7f < self.event_id < 0xa0

            def is_note_off_event(self):
                return 0x8f < self.event_id < 0x90 or (False if len(self.data) < 2 else self.data[1] == 0) #checked in note channel id == 0x8 or velocity == 0
                
            @classmethod
            def ChannelEvent(cls, delta_time, event_id, channel_no = None, params = ()):
                evti = mutils.ch_event_id(event_id, channel_no) if channel_no is not None else event_id 
                # print("Ch event  evti : ", evti, ", None : ", channel_no is None)
                evt = cls(delta_time, constant.CHANNEL_EVENT, evti)
                evt.data = bytearray(params)
                return evt

            
            @classmethod
            def MetaEvent(cls, delta_time, meta_event_type, params = ()):
                evt = cls(delta_time, constant.META_EVENT, 0xff, meta_event_type & 0xff)
                if params is None : return evt
                elif type(params) == str :                    
                    evt.data = params.encode('utf-8')
                else : evt.data = bytearray(params)
                return evt

            @classmethod
            def SysEvent(cls, delta_time, event_id, params = ()):
                evt = cls(delta_time, constant.SYS_EVENT, event_id & 0xff)
                evt.data = bytearray(params)
                return evt
            
            def to_byte_array(self):
                byte_list = bytearray()
                byte_list.extend(mutils.to_var_length(self.delta_time))
                byte_list.append(self.event_id)
                if self.etype == constant.CHANNEL_EVENT:
                    # print("ch : ", self.event_id)
                    # byte_list.pop()
                    # evti = mutils.ch_event_id(self.event_id, self.channel_no)
                    # byte_list.append(evti)
                    pass
                elif self.etype == constant.META_EVENT:
                    byte_list.append(self.meta_event_type)
                    byte_list.extend(mutils.to_var_length(len(self.data)))
                    pass
                elif self.etype == constant.SYS_EVENT:
                    byte_list.extend(mutils.to_var_length(len(self.data)))
                    pass
                # print(self.data)
                byte_list.extend(self.data)
                self.bytes.extend(byte_list)
                self.length = len(self.bytes)
                # hex_string = "".join("%02x" % b for b in byte_list)
                # print("E--> ", hex_string)
                return byte_list
            def leng(self, data = True):
                if data : return len(self.data)
                return len(self.to_byte_array())
            
            def to_dict(self):
                result = {}
                if self.etype == constant.CHANNEL_EVENT:
                    result.update({
                        'type' : X[self.event_id >> 4]['name'],
                        'deltatime' : self.delta_time, 
                        'event_id' : self.event_id,
                        'time' : self.abstime,
                        'duration' : self.elength,
                        'is_drum' : False if (self.event_id & 0xF) != 10 else True,
                    })
                    if self.event_id >> 4 in [0x8, 0x9] :
                        result.update({
                            'pitch' : self.data[0],
                            'velocity' : self.data[1]
                        })
                    else:
                        result.update({
                            "length" : len(self.data),
                            'data' : self.data
                        })
                    if self.event_id >> 4 & 0xF == 0xB: 
                        result.update({'subtype' : X[self.event_id >> 4].get(self.data[0], {}).get("cntrl_name", None)})
                elif self.etype == constant.META_EVENT:
                    result.update({
                        'type' : "meta",
                        'deltatime' : self.delta_time,
                        'time' : self.abstime,
                        'duration' : self.elength,
                        'subtype' : X[0xFF].get(self.meta_event_type, {}).get("type_name", None),
                        'length' : len(self.data),
                        'data' : self.data
                    })
                    pass
                elif self.etype == constant.SYS_EVENT:
                    result.update({
                        'type' : X[self.event_id >> 4]['name'],
                        'deltatime' : self.delta_time,
                        'event_id' : self.event_id,
                        'time' : self.abstime,
                        'duration' : self.elength,
                        'length' : len(self.data),
                        'data' : self.data
                    })
                    pass
                return result

            def __repr__(self):
                # print("E--> ", hex_string)
                # mhxmet = hex(self.meta_event_type) if self.meta_event_type else '0'
                # return "Delta Time : " + hex(self.delta_time) + ", Etype : " + self.etype + ", Event ID : " + hex(self.event_id) + ", META : " + mhxmet + ", Length : " + hex(self.leng()) + ", Data --> " + mutils.hexstr(self.data, group= 2)
                mstr = '______________________________________________________________________________________________________________________________ . . . \n'
                mstr += '| Absolute Time   |  Duration       |  Delta Time |  ETYPE     |   Event ID | META  | LENGTH     | DATA \n' #% (e.abstime, e.elength, hex(e.delta_time), e.etype, hex(e.event_id), mhxmet, hex(e.leng()),  mutils.hexstr(e.data, group= 2))
                mstr += '|______________________________________________________________________________________________________________________________ . . . \n'
                mhxmet = hex(self.meta_event_type) if self.meta_event_type else '0'
                # estr = " Abs Time : " + str(e.abstime) + "Duration : " + str(e.elength) + " |||>>>> Delta Time : " + hex(e.delta_time) + ", Etype : " + e.etype + ", Event ID : " + hex(e.event_id) + ", META : " + mhxmet + ", Length : " + hex(e.leng()) + ", Data --> " + mutils.hexstr(e.data, group= 2)
                estr = '| %-15f | %-15f | %-11s | %-10s | %-10s | %-5s | %-10s |  %s' % (self.abstime, self.elength, hex(self.delta_time), self.etype, hex(self.event_id), mhxmet, hex(self.leng()),  mutils.hexstr(self.data, group= 2))
                return estr