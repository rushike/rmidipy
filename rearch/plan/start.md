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
    d. It may have propeties like length, tostring, matchbytes, matchstring, dytpe etc

4. ByteBlock
    a. Common Structure
    b. It hold raw bytes from file on any type
    c. Each attribute has **startbit** and **endbit** values in block. 
    d. Has length property , value in bytes


5. MidiTrack
    a. It will strore entire MIDI track

6. MidiEvent
    b. It hold MIDI Event