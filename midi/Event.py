from Constant import Constant 
import mutils
class Event :
    
    def __init__(self, delta_time = 0, etype = None, event_id = None, meta_event_type = None, length = 0, data = bytearray()):
        self.delta_time = delta_time
        self.etype = etype
        self.event_id = event_id
        self.meta_event_type = meta_event_type
        self.length = length
        self.data = data
        self.bytes = bytearray()
        
    @classmethod
    def ChannelEvent(cls, delta_time, event_id, channel_no, param = ()):
        evt = cls(delta_time, Constant.CHANNEL_EVENT, mutils.ch_event_id(event_id, channel_no))
        evt.data = param
        return evt

    
    @classmethod
    def MetaEvent(cls, delta_time, meta_event_type, param = (0)):
        evt = cls(delta_time,Constant.META_EVENT, 0xff, meta_event_type & 0xff)
        if type(param) == 'string' :
            evt.data = param.encode('utf-8')
        else : evt.data = bytearray(param)
        return evt

    @classmethod
    def SysEvent(cls, delta_time, event_id, param = ()):
        evt = cls(delta_time, Constant.SYS_EVENT, event_id & 0xff)
        evt.param = param
        return evt
    
    def to_byte_array(self):
        byte_list = bytearray()
        byte_list.extend(mutils.to_var_length(self.delta_time))
        byte_list.extend(mutils.to_var_length(self.event_id))
        if self.etype == Constant.CHANNEL_EVENT:
            pass
        elif self.etype == Constant.META_EVENT:
            byte_list.extend(self.meta_event_type)
            byte_list.extend(len(self.data))
            pass
        elif self.etype == Constant.SYS_EVENT:
            byte_list.extend(len(self.data))
            pass
        byte_list.extend(self.data)
        self.bytes.extend(byte_list)
        self.length = len(self.bytes)
        return byte_list
    def leng(self):
        return len(self.to_byte_array())
