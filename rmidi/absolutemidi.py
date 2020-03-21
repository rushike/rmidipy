from rmidi import MIDI
from rmidi import constant
from rmidi.constant import *
import copy
from rmidi import mutils
class AbsoluteMidi(MIDI):
    def __init__(self, format_type=0, track_count=0, time_div=480, empty=False, filename=None, tempo = 500000):
        super().__init__(format_type=format_type, track_count=track_count, time_div=time_div, empty=empty, filename=filename) # no tempo change assumed glich
        self.tempo = tempo
        
    @classmethod
    def to_abs_midi(cls, midi = MIDI()):
        absmidi = copy.deepcopy(midi)
        # absmidi = midi
        abtime = 0
        tempo = 500000
        time_div = absmidi.time_div
        event_trk = [AbsoluteMidi.AbsoluteTrack(absmidi, empty= True) for _ in range(absmidi.track_count)]
        # print(event_trk[0] is event_trk[1])
        for i, t in enumerate(absmidi.tracks):
            trk = event_trk[i]
            evts = []
            top = 0
            timekeeper = 0 #In milliseconds
            for e in t.trk_event:
                delt = e.delta_time
                if e.event_id == 0xFF : #Meta Event
                    if e.meta_event_type == 0x51: #set_tempo event
                        tempo = mutils.toint(e.data, 8)
                        e.abstime = timekeeper
                        e.elength = 0
                elif 0x7F <  e.event_id < 0xa0: #Note OFF / ON event
                    eventid = e.event_id >> 4
                    noteval = e.data[0]
                    velocity = e.data[1] 
                    timekeeper += (delt/time_div * tempo) / 60000
                    if eventid & 0xF == 9 and velocity != 0: #Note ON event
                        e.abstime = timekeeper
                        evts.append((e, top))

                    elif (eventid  & 0xF == 8) or velocity == 0: # Note OFF event
                        if not evts: raise ValueError("Note OFF Event Occured without the correspoint Note ON Event : ")
                        e_shot = evts.pop()
                        #trk.trk_event[e_shot[1]].elength = timekeeper - trk.trk_event[e_shot[1]].abstime
                        e_shot[0].elength = timekeeper - e_shot[0].abstime
                        continue #to avoid top ++, since Note OFF just update correspoind Note ON value
                else :
                    e.abstime = timekeeper
                    e.elength = 0

                trk.trk_event.append(e)
                top += 1
        # print(tempo)
        amidi = cls(absmidi.format_type, absmidi.track_count, absmidi.track_count, tempo = tempo)
        amidi.tracks = event_trk
        return amidi

    def __repr__(self):
        et = 0
        mstr = ""
        for t in self.tracks:
            # print(mstr)
            mstr += '______________________________________________________________________________________________________________________________ . . . \n'
            mstr += '| Absolute Time   |  Duration       |  Note  Time         |  Delta Time |  ETYPE     |   Event ID | META  | LENGTH     | DATA \n' #% (e.abstime, e.elength, hex(e.delta_time), e.etype, hex(e.event_id), mhxmet, hex(e.leng()),  mutils.hexstr(e.data, group= 2))
            mstr += '|______________________________________________________________________________________________________________________________ . . . \n'
            for e in t.trk_event:
                et += 1
                mhxmet = hex(e.meta_event_type) if e.meta_event_type else '0'
                # estr = " Abs Time : " + str(e.abstime) + "Duration : " + str(e.elength) + " |||>>>> Delta Time : " + hex(e.delta_time) + ", Etype : " + e.etype + ", Event ID : " + hex(e.event_id) + ", META : " + mhxmet + ", Length : " + hex(e.leng()) + ", Data --> " + mutils.hexstr(e.data, group= 2)
                estr = '| %-15f | %-15f | %-20s | %-11s | %-10s | %-10s | %-5s | %-10s |  %s' % (e.abstime, e.elength,mutils.nth_note(e.elength, self.tempo), hex(e.delta_time), e.etype, hex(e.event_id), mhxmet, hex(e.leng()),  mutils.hexstr(e.data, group= 2))
                mstr += (estr + "")
            mstr += '*******************************************************************************************************************\n\n'
        # le = len(mstr)
        # print(le, "  last : ", mstr[le - 1000: le])
        return mstr
    def to_rmidi(self):
        raise NotImplementedError("Not implemeted till now")

    class AbsoluteTrack(MIDI.Track):
        def __init__(self, midi, empty=False):
            super().__init__(midi, empty=empty)

        def _add_event(self, evt):
            self.trk_event.append(evt)

        def add_events_from_dict(self, trackdict = {}):
            for _, event in trackdict.items():
                self._add_event(AbsoluteMidi.AbsoluteTrack.AbsoluteEvent.from_dict(**event))

        class AbsoluteEvent(MIDI.Track.Event):
            def __init__(self, delta_time=0, etype=None, event_id=None, meta_event_type=None, length=0, data=bytearray()):
                    super().__init__(delta_time=delta_time, etype=etype, event_id=event_id, meta_event_type=meta_event_type, length=length, data=data)
            
            @classmethod
            def from_dict(cls, **kparams):
                if not {"time", "duration", "type", "deltatime"} < set(kparams):
                    raise AttributeError(f"Attribute dict not of correct format : {kparams}")
                subtype = kparams.get('subtype', "None")
                if kparams["type"] in ch_events:
                    # for now data is specially note_on or note_off event
                    data = kparams["data"] if "data" in kparams else [kparams["pitch"], kparams["velocity"]]
                    event = cls.ChannelEvent(delta_time = kparams["deltatime"], event_id = kparams["event_id"], 
                            params=data)
                elif kparams["type"] in sMETA_EVENT: # checking type is meta, since all meta event has same event id
                    if subtype in meta_events:
                        index, _ = mutils.find_location(subtype, constant.meta_event_format)
                        event = cls.MetaEvent(delta_time = kparams["deltatime"], meta_event_type=constant.meta_event_format[index][0], params= kparams["data"])
                    else: raise AttributeError(f"Do not have appropiate <Meta.subtype>, subtype : {kparams.get('subtype', 'None')}")
                elif kparams['type'] in sys_events:
                        event = cls.SysEvent(delta_time = kparams["deltatime"], event_id = kparams["event_id"], params=kparams["data"])
                else: raise AttributeError(f"kparams <type> param invalid, type : {kparams['type']}")
                event.abstime = kparams["time"]
                event.elength = kparams["duration"]
                return event
