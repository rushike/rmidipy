# rmidipy
This python library is intended to open midi files as python objects. Midi file is binary files, _list_ in form of tracks.
Every _track_ contains sequence of __events__. Each __event__ is assosiated __*delta time*__, which refers to time from perivous 
event, current event should occur.

In same structure __*rmidi*__  has `MIDI` as base class, `MIDI.Track` for track representation and `MIDI.Track.Event` to represent each event.
## Getting Started
`rmidi` is available on `python pip`. You can install library through below command.
```cmd
    $ pip install rmidi
```

## MIDI 
```python
>>> from rmidi import MIDI
>>> y = MIDI.parse_midi(<midi_file_path>)
```

**OUTPUT**
```_____________________________________________________________________________________________________________________________ . . .
| Absolute Time   |  Duration       |  Delta Time |  ETYPE     |   Event ID | META  | LENGTH     | DATA
|______________________________________________________________________________________________________________________________ . . .
| 0.000000        | 0.000000        | 0x0         | META       | 0xff       | 0x58  | 0x4        |  0x04  0x02 0x18  0x08

| 0.000000        | 0.000000        | 0x0         | META       | 0xff       | 0x59  | 0x2        |  0x00  0x00

| 0.000000        | 0.000000        | 0x0         | META       | 0xff       | 0x51  | 0x3        |  0x07  0xa1 0x20

| 0.000000        | 0.000000        | 0x0         | CHANNEL    | 0xb0       | 0     | 0x2        |  0x79  0x00

| 0.000000        | 0.000000        | 0x0         | CHANNEL    | 0xc0       | 0     | 0x1        |  0x00

| 0.000000        | 0.000000        | 0x0         | CHANNEL    | 0xb0       | 0     | 0x2        |  0x07  0x64

| 0.000000        | 0.000000        | 0x0         | CHANNEL    | 0xb0       | 0     | 0x2        |  0x0a  0x40

| 0.000000        | 0.000000        | 0x0         | CHANNEL    | 0xb0       | 0     | 0x2        |  0x5b  0x00

| 0.000000        | 0.000000        | 0x0         | CHANNEL    | 0xb0       | 0     | 0x2        |  0x5d  0x00

| 0.000000        | 0.000000        | 0x0         | META       | 0xff       | 0x21  | 0x1        |  0x00

| 0.000000        | 0.000000        | 0x0         | CHANNEL    | 0x90       | 0     | 0x2        |  0x48  0x50

| 0.000000        | 0.000000        | 0x71f       | CHANNEL    | 0x90       | 0     | 0x2        |  0x48  0x00

| 0.000000        | 0.000000        | 0x61        | CHANNEL    | 0x90       | 0     | 0x2        |  0x4a  0x50

| 0.000000        | 0.000000        | 0x71f       | CHANNEL    | 0x90       | 0     | 0x2        |  0x4a  0x00

| 0.000000        | 0.000000        | 0x61        | CHANNEL    | 0x90       | 0     | 0x2        |  0x4c  0x50

| 0.000000        | 0.000000        | 0x71f       | CHANNEL    | 0x90       | 0     | 0x2        |  0x4c  0x00

| 0.000000        | 0.000000        | 0x61        | CHANNEL    | 0x90       | 0     | 0x2        |  0x4d  0x50

| 0.000000        | 0.000000        | 0x71f       | CHANNEL    | 0x90       | 0     | 0x2        |  0x4d  0x00

| 0.000000        | 0.000000        | 0x61        | CHANNEL    | 0x90       | 0     | 0x2        |  0x4f  0x50

| 0.000000        | 0.000000        | 0x71f       | CHANNEL    | 0x90       | 0     | 0x2        |  0x4f  0x00

| 0.000000        | 0.000000        | 0x61        | CHANNEL    | 0x90       | 0     | 0x2        |  0x51  0x50

| 0.000000        | 0.000000        | 0x71f       | CHANNEL    | 0x90       | 0     | 0x2        |  0x51  0x00

| 0.000000        | 0.000000        | 0x61        | CHANNEL    | 0x90       | 0     | 0x2        |  0x53  0x50

| 0.000000        | 0.000000        | 0x71f       | CHANNEL    | 0x90       | 0     | 0x2        |  0x53  0x00

| 0.000000        | 0.000000        | 0x61        | CHANNEL    | 0x90       | 0     | 0x2        |  0x54  0x50

| 0.000000        | 0.000000        | 0x71f       | CHANNEL    | 0x90       | 0     | 0x2        |  0x54  0x00

| 0.000000        | 0.000000        | 0x1         | META       | 0xff       | 0x2f  | 0x0        |
```

## Absolute midi
Absolute Midi is defined as its time from start, in seconds.

```python
>>> from rmidi import MIDI, AbosluteMidi
>>> y = MIDI.parse_midi(<midi-file-path>)
>>> yabs = AbsoluteMidi.to_abs_midi(y)
>>> print(yabs)
```

**OUTPUT**
```
| Absolute Time   |  Duration       |  Note  Time         |  Delta Time |  ETYPE     |   Event ID | META  | LENGTH     | DATA
|______________________________________________________________________________________________________________________________ . . .
| 0.000000        | 0.000000        | 0                    | 0x0         | META       | 0xff       | 0x58  | 0x4        |  0x04  0x02 0x18  0x08
| 0.000000        | 0.000000        | 0                    | 0x0         | META       | 0xff       | 0x59  | 0x2        |  0x00  0x00
| 0.000000        | 0.000000        | 0                    | 0x0         | META       | 0xff       | 0x51  | 0x3        |  0x07  0xa1 0x20
| 0.000000        | 0.000000        | 0                    | 0x0         | CHANNEL    | 0xb0       | 0     | 0x2        |  0x79  0x00
| 0.000000        | 0.000000        | 0                    | 0x0         | CHANNEL    | 0xc0       | 0     | 0x1        |  0x00
| 0.000000        | 0.000000        | 0                    | 0x0         | CHANNEL    | 0xb0       | 0     | 0x2        |  0x07  0x64
| 0.000000        | 0.000000        | 0                    | 0x0         | CHANNEL    | 0xb0       | 0     | 0x2        |  0x0a  0x40
| 0.000000        | 0.000000        | 0                    | 0x0         | CHANNEL    | 0xb0       | 0     | 0x2        |  0x5b  0x00
| 0.000000        | 0.000000        | 0                    | 0x0         | CHANNEL    | 0xb0       | 0     | 0x2        |  0x5d  0x00
| 0.000000        | 0.000000        | 0                    | 0x0         | META       | 0xff       | 0x21  | 0x1        |  0x00
| 0.000000        | 31.649306       | 1.0666666666666667   | 0x0         | CHANNEL    | 0x90       | 0     | 0x2        |  0x48  0x50
| 33.333333       | 31.649306       | 1.0666666666666667   | 0x61        | CHANNEL    | 0x90       | 0     | 0x2        |  0x4a  0x50
| 66.666667       | 31.649306       | 1.0666666666666667   | 0x61        | CHANNEL    | 0x90       | 0     | 0x2        |  0x4c  0x50
| 100.000000      | 31.649306       | 1.0666666666666667   | 0x61        | CHANNEL    | 0x90       | 0     | 0x2        |  0x4d  0x50
| 133.333333      | 31.649306       | 1.0666666666666667   | 0x61        | CHANNEL    | 0x90       | 0     | 0x2        |  0x4f  0x50
| 166.666667      | 31.649306       | 1.0666666666666667   | 0x61        | CHANNEL    | 0x90       | 0     | 0x2        |  0x51  0x50
| 200.000000      | 31.649306       | 1.0666666666666667   | 0x61        | CHANNEL    | 0x90       | 0     | 0x2        |  0x53  0x50
| 233.333333      | 31.649306       | 1.0666666666666667   | 0x61        | CHANNEL    | 0x90       | 0     | 0x2        |  0x54  0x50
| 0.000000        | 0.000000        | 0                    | 0x1         | META       | 0xff       | 0x2f  | 0x0        |
*******************************************************************************************************************
```

## NoteSequence
`rmidi.dataset.NoteSequence` is simliar object to that of `Magenta.NoteSequence`, It holds everthing in dict, whole midi file is express as ***python nested dictionary***

```python
>>> from rmidi.dataset import notesequence
>>> ns = NoteSequence(<midi-file-path>)
>>> print(ns)
```

**Output**
```
[
    {
        "track-0": [
            [
                "type : meta",
                "deltatime : 0",
                "time : 0",
                "duration : 0",
                "subtype : time_sig",
                "length : 4",
                "data : 0x04  0x02 0x18 0x08 \n"
            ],
            [
                "type : meta",
                "deltatime : 0",
                "time : 0",
                "duration : 0",
                "subtype : key_sig",
                "length : 2",
                "data : 0x00  0x00 \n"
            ],
            [
                "type : meta",
                "deltatime : 0",
                "time : 0",
                "duration : 0",
                "subtype : set_tempo",
                "length : 3",
                "data : 0x07  0xa1 0x20 \n"
            ],
            [
                "type : cntroller",
                "deltatime : 0",
                "event_id : 176",
                "time : 0",
                "duaration : 0",
                "pitch : None",
                "velocity : None",
                "is_drum : False",
                "subtype : mode_messages_0"
            ],
            [
                "type : program_change",
                "deltatime : 0",
                "event_id : 192",
                "time : 0",
                "duaration : 0",
                "pitch : None",
                "velocity : None",
                "is_drum : False"
            ],
            [
                "type : cntroller",
                "deltatime : 0",
                "event_id : 176",
                "time : 0",
                "duaration : 0",
                "pitch : None",
                "velocity : None",
                "is_drum : False",
                "subtype : main_volume"
            ],
            [
                "type : cntroller",
                "deltatime : 0",
                "event_id : 176",
                "time : 0",
                "duaration : 0",
                "pitch : None",
                "velocity : None",
                "is_drum : False",
                "subtype : pan"
            ],
            [
                "type : cntroller",
                "deltatime : 0",
                "event_id : 176",
                "time : 0",
                "duaration : 0",
                "pitch : None",
                "velocity : None",
                "is_drum : False",
                "subtype : effects_depth_0"
            ],
            [
                "type : cntroller",
                "deltatime : 0",
                "event_id : 176",
                "time : 0",
                "duaration : 0",
                "pitch : None",
                "velocity : None",
                "is_drum : False",
                "subtype : effects_depth_2"
            ],
            [
                "type : meta",
                "deltatime : 0",
                "time : 0",
                "duration : 0",
                "subtype : midi_port",
                "length : 1",
                "data : 0x00  \n"
            ],
            [
                "type : note_on",
                "deltatime : 0",
                "event_id : 144",
                "time : 0.0",
                "duaration : 31.649305555555554",
                "pitch : 72",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 33.33333333333333",
                "duaration : 31.649305555555557",
                "pitch : 74",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 66.66666666666666",
                "duaration : 31.649305555555557",
                "pitch : 76",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 99.99999999999999",
                "duaration : 31.649305555555557",
                "pitch : 77",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 133.33333333333331",
                "duaration : 31.649305555555543",
                "pitch : 79",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 166.66666666666663",
                "duaration : 31.649305555555543",
                "pitch : 81",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 199.99999999999994",
                "duaration : 31.649305555555543",
                "pitch : 83",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 233.33333333333326",
                "duaration : 31.649305555555543",
                "pitch : 84",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : meta",
                "deltatime : 1",
                "time : 0",
                "duration : 0",
                "subtype : end_of_track",
                "length : 0",
                "data : \n"
            ]
        ]
    }
]
```
### NoteSequence@`tostring`
Converts the dict to pretty string
```python
from rmidi.dataset import NoteSequence
dict_ = {0: OrderedDict([(17, {'type': 'note_on', 'deltatime': 97, 'event_id': 144, 'time': 233.33333333333326, 'duaration': 31.649305555555543, 'pitch': 84, 'velocity': 80, 'is_drum': False}), (16, {'type': 'note_on', 'deltatime': 97, 'event_id': 144, 'time': 199.99999999999994, 'duaration': 31.649305555555543, 'pitch': 83, 'velocity': 80, 'is_drum': False}), (15, {'type': 'note_on', 'deltatime': 97, 'event_id': 144, 'time': 166.66666666666663, 'duaration': 31.649305555555543, 'pitch': 81, 'velocity': 80, 'is_drum': False}), (14, {'type': 'note_on', 'deltatime': 97, 'event_id': 144, 'time': 133.33333333333331, 'duaration': 31.649305555555543, 'pitch': 79, 'velocity': 80, 'is_drum': False}), (13, {'type': 'note_on', 'deltatime': 97, 'event_id': 144, 'time': 99.99999999999999, 'duaration': 31.649305555555557, 'pitch': 77, 'velocity': 80, 'is_drum': False}), (12, {'type': 'note_on', 'deltatime': 97, 'event_id': 144, 'time': 66.66666666666666, 'duaration': 31.649305555555557, 'pitch': 76, 'velocity': 80, 'is_drum': False}), (11, {'type': 'note_on', 'deltatime': 97, 'event_id': 144, 'time': 33.33333333333333, 'duaration': 31.649305555555557, 'pitch': 74, 'velocity': 80, 'is_drum': False}), (10, {'type': 'note_on', 'deltatime': 0, 'event_id': 144, 'time': 0.0, 'duaration': 31.649305555555554, 'pitch': 72, 'velocity': 80, 'is_drum': False})])}
print(NoteSequence.tostring(dict_))
``` 
**Output**
```
[
    {
        "track-0": [
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 233.33333333333326",
                "duaration : 31.649305555555543",
                "pitch : 84",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 199.99999999999994",
                "duaration : 31.649305555555543",
                "pitch : 83",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 166.66666666666663",
                "duaration : 31.649305555555543",
                "pitch : 81",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 133.33333333333331",
                "duaration : 31.649305555555543",
                "pitch : 79",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 99.99999999999999",
                "duaration : 31.649305555555557",
                "pitch : 77",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 66.66666666666666",
                "duaration : 31.649305555555557",
                "pitch : 76",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 33.33333333333333",
                "duaration : 31.649305555555557",
                "pitch : 74",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 0",
                "event_id : 144",
                "time : 0.0",
                "duaration : 31.649305555555554",
                "pitch : 72",
                "velocity : 80",
                "is_drum : False"
            ]
        ]
    }
]
```
### NoteSequence@`notes`
To get just notes, i.e. just **note_on** and **note_off** event, you can call `NoteSequence` object as `ns.notes`
```python
>>> from rmidi.dataset import NoteSequence
>>> ns = NoteSequence(<midi-file-path>)
>>> notes = ns.notes
>>> print(notes)
>>> print(ns.tostring(notes)) # to pretty print
```
**Output**
```
 [
    {
        "track-0": [
            [
                "type : note_on",
                "deltatime : 0",
                "event_id : 144",
                "time : 0.0",
                "duaration : 31.649305555555554",
                "pitch : 72",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 33.33333333333333",
                "duaration : 31.649305555555557",
                "pitch : 74",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 66.66666666666666",
                "duaration : 31.649305555555557",
                "pitch : 76",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 99.99999999999999",
                "duaration : 31.649305555555557",
                "pitch : 77",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 133.33333333333331",
                "duaration : 31.649305555555543",
                "pitch : 79",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 166.66666666666663",
                "duaration : 31.649305555555543",
                "pitch : 81",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 199.99999999999994",
                "duaration : 31.649305555555543",
                "pitch : 83",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 233.33333333333326",
                "duaration : 31.649305555555543",
                "pitch : 84",
                "velocity : 80",
                "is_drum : False"
            ]
        ]
    }
]
```

### Notesequence@`order_by`
It orders the events within track base on event attribute, order by is intended to work for attributes 'time', 'duration', 'pitch', deltatime
```python
>>> from rmidi.dataset import NoteSequence
>>> ns = NoteSequence(filepath)
>>> ordered = ns.order_by(<attribute_name>, reverse=True)
>>> print(ordered) # Output for pitch sorted in reverse
```

**Output**
```
$
[
    {
        "track-0": [
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 233.33333333333326",
                "duaration : 31.649305555555543",
                "pitch : 84",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 199.99999999999994",
                "duaration : 31.649305555555543",
                "pitch : 83",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 166.66666666666663",
                "duaration : 31.649305555555543",
                "pitch : 81",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 133.33333333333331",
                "duaration : 31.649305555555543",
                "pitch : 79",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 99.99999999999999",
                "duaration : 31.649305555555557",
                "pitch : 77",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 66.66666666666666",
                "duaration : 31.649305555555557",
                "pitch : 76",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 97",
                "event_id : 144",
                "time : 33.33333333333333",
                "duaration : 31.649305555555557",
                "pitch : 74",
                "velocity : 80",
                "is_drum : False"
            ],
            [
                "type : note_on",
                "deltatime : 0",
                "event_id : 144",
                "time : 0.0",
                "duaration : 31.649305555555554",
                "pitch : 72",
                "velocity : 80",
                "is_drum : False"
            ]
        ]
    }
]
```

### Notesequence@`to_abs_midi`
Convert `NoteSequece` to `AbsoluteMidi` object.
```python
>>> from rmidi.dataset import NoteSequence
>>> ns = NoteSequence(filepath)
>>> absmidi = ns.to_abs_midi()
>>> print(type(absmidi))
```
**Output**
```$
<class 'rmidi.absolutemidi.AbsoluteMidi'>
```