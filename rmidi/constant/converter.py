from rmidi.constant import Constants
import os
import json
def dict_to_event_json(filename, dictn):
    with open(filename, 'w') as wrt:
        str_ = json.dumps(dictn, indent=4)
        wrt.write(str_)

def to_channel_event_dict():
    '''
        id : Midi Channel Event Id
        name : Corresponding Midi Event Name
        length : length of parameters needed
        params : list of parameter values, Big-Endian format; 0 indicates most significant bit
        mask : bitmask over the 8 bit value; It can be list or sin 
    '''
    ch_dict = {}
    key = ['id', 'name', 'length', 'params', 'mask']
    for row in Constants.ch_event_format:
        rw0 = row[0]
        if rw0 == 0xB:
            ch_dict[rw0] = to_ch_controller_dict()
            continue
        ch_dict[rw0] = {}
        for i, k in enumerate(key[:3]):
            ch_dict[rw0][k] = row[i]
        ch_dict[rw0]['params'] = row[3: 3 + row[2]]
        ch_dict[rw0]['mask'] = 127 if row[3 + row[2]] == 'int' else row[3 + row[2]: ]

    return ch_dict

def to_meta_event_dict():
    '''
        id : Midi Channel Event Id, Always (0xFF)
        name : Corresponding Midi Event Name, Always meta
        type_id: Midi Meta Event Sub Type Id
        type_name: Midi Meta Event Sub Type Name
        length : length of parameters needed
        params : list of parameter values, Big-Endian format; 0 indicates most significant bit
        mask : bitmask over the 8 bit value; It can be list or sin 
    '''
    meta_dict = {0xFF : {'id' : 0xFF, 'name': 'meta'}}
    key = ['type_id', 'type_name', 'length', 'params', 'mask']
    for row in Constants.meta_event_format:
        rw0 = row[0]
        meta_dict[0xFF][rw0]= {}
        for i, k in enumerate(key[:3]):
            meta_dict[0xFF][rw0][k] = row[i]
        meta_dict[0xFF][rw0]['params'] = row[3: 3 + row[2]] if row[2] != 0 and row[2] != -1 else None if row[2] == 0 else 'text'
        meta_dict[0xFF][rw0]['dtype'] = row[4] if row[2] == 0 or row[2] == -1 else row[3 + row[2]] #  127 if row[3 + row[2]] == 'str' else None #row[3 + row[2]] if row[2] != 0 or row[2] != -1 else row[4]  
        meta_dict[0xFF][rw0]['mask'] = row[4 + row[2] : ] if row[3 + row[2]] == 'int' else None if row[4] == None else 127 # row[4 + row[2]: ]

    # print(meta_dict)
    return meta_dict

def to_sys_event_dict():
    sys_dict = {}
    key = ['id', 'name', 'length', 'params', 'dtype', 'mask']
    for e in Constants.sys_event_format:
        sys_dict[e[0]] = {}
        for i, k in enumerate(key):
            sys_dict[e[0]][k] = e[i] 
    # print(sys_dict)
    return sys_dict

def to_ch_controller_dict():
    '''
        cntrl_id : Midi Channel Controller Event Subtype Id
        cntrl_name : Corresponding Midi Controller Event Subtype Name
    '''
    cntrl = Constants.controller
    res = {
        "id": 0xB,
        "name": "controller",
        "length": 2,
        "params": [
            "controller_type",
            "value"
        ],
        "mask": 127
    }
    for cnt in cntrl:
        if cnt[2] == 1: 
            b = 1
            res[cnt[0]] = {'cntrl_id' : cnt[0], 'cntrl_name' : cnt[1]}  
        else :
            b = 0
            res[cnt[0]] = {}

        for ky in range(cnt[0] + b, cnt[0] + cnt[2]):
            res[ky] = {'cntrl_id' : ky, 'cntrl_name' : cnt[1] + '_' + str(ky - cnt[0])}

    # print(res)
    return res

def write_dict(dictn, filename, variable_name = 'X'):
    pass

# def ch_event_format():
#     f = './rmidi/constant/ch_event_format.json'
#     # f = './ch_event_format.json.py'
#     exists = os.path.exists(f)
#     with open('./rmidi/constant/ch_event_format.json', 'r') as f:
#         return json.load(f.read())

# def meta_event_format():
#     f = '.\\rmidi\\constant\\meta_event_format.json'
#     # f = './meta_event_format.json.py'
#     exists = os.path.exists(f)
#     print(exists, "   ", os.listdir())
#     with open(f, 'r+') as fil:
#     # st = fil.read()
#     # fil.close()
#         res = json.load(fil)


#     return res

# def sys_event_format():
#     # f = './rmidi/constant/'
#     with open('./rmidi/constant/sys_event_format.json.py', 'r') as f:
#         return json.load(f.read())

# ch_event = to_channel_event_dict()
# dict_to_event_json('./rmidi/constant/ch_event_format.json', ch_event)

# meta_event = to_meta_event_dict()
# dict_to_event_json('./rmidi/constant/meta_event_format.json', meta_event)

# # ch_cntrl_event = to_ch_controller_dict()
# # dict_to_event_json('./rmidi/constant/ch_controller.json', ch_cntrl_event)

# sys_event = to_sys_event_dict()
# dict_to_event_json('./rmidi/constant/sys_event_format.json', sys_event)