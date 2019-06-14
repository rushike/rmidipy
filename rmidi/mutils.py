import math, re
import numpy
import hashlib as ha

hash_ =  ha.md5()

WRAP_DATA = 0x7f
WRAP_BITS = 7


def ch_event_id(id, no) :
    return ((id & 0xf) << 4) | (no & 0xf)

def channel(evt_id):
    return (evt_id >> 4) & 0xf
    
def numin(num, startb, off):#off length of bits that want
    return (num >> startb) & ((1 << off) - 1)

def meta_event_type(typ):
    return typ & 0xff

def to_var_length(k):
    if k > 127:
        leng = length(k) // WRAP_BITS + 1
        var = bytearray(leng)
        var[-1] = k & WRAP_DATA
        k >>= WRAP_BITS
        for i in range(leng - 2, -1, -1):
            var[i] = (k & WRAP_DATA) | (1 << WRAP_BITS )
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
            # fix[i] = (k & wrapper) + wrapper + 1
            fix[i] = k & wrapper
            k >>= bits
    elif k > -1 :
        fix[-1] = k & 0xff
    return fix


def vartoint(varray:bytearray()):
    return toint(varray, 7)
def toint(a : bytearray(), bits = 8, mode = 'BG'):
    WRAPPER = (1 << bits) - 1
    num, itr, ind, s, le = 0x00, 0, 0, 1, len(a)
    if mode == 'LL': #set loop from end for little indian  
        s, ind= -1, le - 1
    while itr < le and ind < le:
        num = (num << bits) | (a[ind] & WRAPPER)
        ind += s
        itr += 1
    return num


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

def match(whole:bytearray, pattern= bytearray):
    return re.search(pattern, whole)

def find_location(text, listt):
    try:
        return next((i, j) 
            for i, t in enumerate(listt)
            for j, v in enumerate(t)
            if v == text)
    except StopIteration:
        return None

# @param num byte array to be converted
# @param type type : big-endian or small-endian
# @param group no. of bytes in group
# @param length length of line(in bytes)
# @return
def hexstr(bnum: bytearray, leng = 0, group = 0, numlen = 2, ftype = 0):
    if ftype == 1: bnum = bnum.reverse()
    if group == 0: group = len(bnum)
    if leng == 0: leng = len(bnum)    
    st = ''
    for i in range(len(bnum)):
        x = hex(bnum[i])[2:]
        if len(x) != numlen: x = "0" * (numlen - len(x)) + x[:2]
        st += ('0x' + x + ' ')
        if i % group == 0: st += ' '
        if (i + 1) % leng == 0: st += '\n'
    return st

def dtime(delta_time, time_div):
    if not delta_time: return 0
    return int((time_div * 4) // delta_time)


def file_hash(f, hexst = False):
    with open(f, "rb") as fi:
        cont = fi.read()
        return ha.md5(cont).hexdigest()
    return hash_.hexdigest()

def midi_to_note(noteval):
    if not numpy.isscalar(noteval): return [midi_to_note(v) for v in noteval]

    if not 20 < noteval < 128: raise ValueError('Noteval not in range : {}'.format(noteval))
    
    mod = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
    
    note = mod[noteval % 12]
    octave = noteval // 12 - 1
    return '{}{}'.format(note, octave)

def note_to_midi(note):
    val_notes = {'c' : 0, 'c#' : 1, 'd' : 2, 'd#': 3, 'e': 4, 'f': 5, 'f#': 6, 'g': 7, 'g#': 8, 'a': 9, 'a#': 10, 'b': 11}
    if not numpy.isscalar(note): return [note_to_midi(v) for v in note]
    
    if note[:2].lower() not in val_notes: raise ValueError('Invalid Note String {}'.format(note))

    note, octave = note[:2], note[2:]


def dictn(ndlist):
    return {l[0] : l[1:]  for l in ndlist}
