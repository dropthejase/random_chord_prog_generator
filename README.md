# random_chord_prog_generator
A random chord progression generator which can generate random 4/4 chord progressions with different rhythmic basslines. Can also export as MIDI. Final project for CS50's Introduction to Computer Science.


##### Introduction - A tool to combat writer's block!
This random chord progression generator is used as a simple standalone application for generator random chord progressions in 4/4 signature.
This tool is geared towards music producers looking to create contemporary, radio-friendly music (e.g. pop, RnB, EDM...etc.)
Use it to generate baselines or chord triads, with a variety of different rhythmic options, and export as MIDI to drop into your DAW.
You can also choose the key and BPM for the playback so you can test baselines whilst having your music project open!


###### Overview
I made this tool as a way of putting my Python skills (which I picked up several months ago) into practice and as my final project for Harvard CS50 course!

The tool imports from the following libraries:

- tkinter to create the GUI
- midiutil to create the MIDI files and export
- pygame to playback MIDI files so you can preview the chord progression / rhythmic choice
- random for a variety of functions including picking random chords from the list of available chords to create the chord progression, as well as to randomise the rhythm

The GUI should be quite self-explanatory but below is an overview of how to use this tool...


##### Generate Progression
Simply hit 'Generate Progression' to generate new chord progressions.
The chords available in this version are I, ii, iii, IV, V, and VI (lowercase numbers mean minor chords).
Although some might argue that this selection is somewhat limited, these tend to be the most common chords used in contemporary music.

To make this, I essentially created a list with some chords, and used the random library to iterate through it to pull out four random chords, which is stored in a temporary list.
I also coded it such that no two identical chords would play one after the other.


##### BPM
Use this BPM sliding scale to match the BPM to your project's BPM to help you understand how the chords generated might fit with your project.
Alternatively, use it to see how a progression might sound at different speeds to see if it might spark some ideas.

This simply comprises a Tkinter Scale widget, in which the value is pulled by a bpm_read() function which returns the BPM


##### Scale
You can set to your desired key

This simply comprises a Tkinter OptionMenu widget, in which the value is pulled by a key_read() function which eventually returns a constant.
Given the default key is C major, this constant is added to the pitch of the MIDI notes to transpose the key as desired.


##### Bassline Rhythm
Choose between standard rhythm options, or select 'Randomise' if you need help with creating inspiring rhythms!

To incorporate this, as well as the BPM and Scale above, I created two separate functions to store the rhythm (which comprises a timestamp, note duration, and note quantity) into the MIDI file.
One function, midi(), writes the MIDI file where a simple, predetermined rhythm is selected (i.e. all the options except 'Randomise').
The other, randomise(), randomly assigns durations to the MIDI notes created.

Finally, buildtrack() opens up these dictionaries and writes them into MIDI objects. One MIDI object, mf, is simply used for a single 'Root Note Only' baseline.
Another, mf_chord, is used for the 'Chord/Triad' option.


##### Play
Hit 'Play' to preview the chord progression.

This uses a MIDIUtil object and creates a copy of either the mf or mf_chord object depending on above 'Root Note Only' or 'Chord/Triad' selection.
The MIDI object is then exported.
Pygame is then used to playback the MIDI object using a generic 'bass synth' sound from the general Windows Soundfiles. 


##### Export MIDI
Finally, hit this button to export your chord progression as a MIDI file to drop into your DAW!

This uses a simple writeFile() method from MIDIUtil.
