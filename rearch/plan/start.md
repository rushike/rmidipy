# rmidi rearch

## Top Level
Should have following classes

1. MIDIStream
    a. It should able to connect to extrenal system and recieve the live MIDI events / bytes
    
2. MIDI
    b. It is offline representation of MIDI file. We have entire file by now.

3. ByteChunk
    a. Common Structure
    b. It hold raw bytes from file. 
    c. It can hold entire file or part of file
    d. Has length property , value in bytes
    e. Has content property where actual bytes are stored
    f. It may have propeties like length, tostring, matchbytes, matchstring, dytpe etc

4. ByteBlock
    a. Common Structure
    b. It hold raw bytes from file on any type
    c. Has length property , value in bytes
    d. Has content property where actual bytes are stored


5. Midi
    a. It store entire midi file as python object

6. MidiHeader
    a. It store midi header (MThd) as python object

7. MidiTrack
    a. It will strore entire MIDI track (MTrk) as python object
    b. It will have functionality of timeline, i.e. arranging midi event in timeline

8. MidiEvent
    b. It hold MIDI Event as python object



 ## Parser
1. MidiParser
    a. Base class for all Sub Midi Parser

2. MIDI
    a. It will read file from **reader** object and start parsing MIDI

3. MidiHeaderParser
    a. It will parse midi header

4. MidiTrackParser
    a. It will parse midi track

5. MidiEventParser
    a. It will parse midi event


## Reference 
1. Standard MIDI-File Format Spec. 1.1, updated (http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html)