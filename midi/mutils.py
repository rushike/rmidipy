import math
WRAP_DATA = 0x7f
WRAP_BITS = 7

def ch_event_id(id, no) :
    return ((id & 0xf) << 4) + (no & 0xf)

def meta_event_type(typ):
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

def length(k):
    """Finds length of k in bits
    
    Arguments:
        k {int} -- Integer number
    """
    return int(math.log2(k) + 1)

