# rmidi rearch

## Top Level
Should have following classes

1. MIDIStream
    - It should able to connect to extrenal system and recieve the live MIDI events / bytes
    
2. MIDI
    - It is offline representation of MIDI file. We have entire file by now.

3. ByteChunk
    - Common Structure
    - It hold raw bytes from file. 
    - It can hold entire file or part of file
    - Has length property , value in bytes
    - Has content property where actual bytes are storeď
    - It may have propeties like length, tostring, matchbytes, matchstring, dytpe etc

4. ByteBlock
    - Common Structure
    - It hold raw bytes from file on any type
    - Has length property , value in bytes
    - Has content property where actual bytes are stored


5. Midi
    - It store entire midi file as python object

6. MidiHeader
    - It store midi header (MThd) as python object

7. MidiTrack
    - It will strore entire MIDI track (MTrk) as python object
    b. It will have functionality of timeline, i.e. arranging midi event in timeline

8. MidiEvent
    b. It hold MIDI Event as python object


## Reader
1. Reader
    - Base class for all reader object

2. FileReader
    - Able to read bytes from file and store in memory

3. BufferReader
    - Able to read bytes as file and store in memory


 ## Parser
1. MidiParser
    - Base class for all Sub Midi Parser

2. MIDI
    - It will read file from **reader** object and start parsing MIDI

3. MidiHeaderParser
    - It will parse midi header

4. MidiTrackParser
    - It will parse midi track

5. MidiEventParser
    - It will parse midi event


## Reference 
1. Standard MIDI-File Format Spec. 1.1, updated (http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html)