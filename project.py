#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk

from midiutil import MIDIFile
import pygame

import random

### LISTS ###

# MASTER #
chords = ['I', 'ii', 'iii', 'IV', 'V', 'vi']
chords_weight = [] # ? maybe another time
midi_note_number = [60, 62, 64, 65, 67, 69]

#MIDI stuff

fifth = 5

duration_temp = {}
half_temp = {}

# TEMPORARY #
progr = ['I', 'I', 'I', 'I']
midi_note = [60, 60, 60, 60]
third = [8, 8, 8, 8]

mf = MIDIFile(1)
mf_chord = MIDIFile(1)
track = 0
tempo = 120
mf.addTrackName(track, 0, 'Sample Track')
mf.addTempo(track, 0, tempo)

mf_chord.addTrackName(track, 0, 'Sample Track')
mf_chord.addTempo(track, 0, tempo)

channel = 0
volume = 100

### Functions ###

def generate():
    
    #global progr
    #global midi_note
    #global third
    #global duration_temp
    
    prog = [] # needs temporary list so we can clear it?
    for i in range(4):
        if i == 0:
            prog.append(random.choice(chords)) # first chord = any
        else:
            prog.append(random.choice(chords)) # make sure next chord is different
            while prog[i] == prog[i-1]:
                prog[i] = random.choice(chords)
        progr[i] = prog[i]
        midi_note[i] = midi_note_number[chords.index(prog[i])]
        
        if midi_note[i] in [62, 64, 69]:
            third[i] = 9
        else:
            third[i] = 8
        
    text = '|  '
    for i in range(len(prog)):
        text += prog[i] + '  |  '
    generated['text'] = text
    
    if var.get() < 4:
        midi()
    elif not duration_temp:
        randomise()
    else:
        buildtrack()

def bpm_read():
    
    n = int(bpm_scale.get())
    return n

def key_read():
    
    key_dict = {
        'C / Amin' : 0,
        'G / Emin' : 7,
        'D / Bmin' : 2,
        'A / F#min' : 9,
        'E / C#min' : 4,
        'B / G#min' : 11,
        'F# / Ebmin' : 6,
        'C# / Bbmin' : 1,
        'Ab / Fmin' : 8,
        'Eb / Cmin' : 3,
        'Bb / Gmin' : 10,
        'F / Dmin' : 5}
    
    k = key_dict[key_var.get()]
    
    return k
    
def play():

    global mf
    global mf_chord
    
    if var.get() < 4 and var_root.get() == 0:
        midi()
        buildtrack()
        temp_mf = mf
    elif var.get() < 4 and var_root.get() == 1:
        midi()
        buildtrack()
        temp_mf = mf_chord
    elif var.get() == 4 and var_root.get() == 0:
        buildtrack()
        temp_mf = mf
    elif var.get() == 4 and var_root.get() == 1:
        buildtrack()
        temp_mf = mf_chord
    
    n = bpm_read()
    temp_mf.addTempo(track, 0, n)
    
    temp_mf.addProgramChange(0, 0, 0, 39) # adds synth bass

    with open('temp.mid', 'wb') as outf:
        temp_mf.writeFile(outf)
    
    freq = 44100  # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 1024   # number of samples
    
    clock = pygame.time.Clock()
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.load('temp.mid')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(60)
       
def generate_rhythm_enable():
    rhythm_randomise_button['state'] = 'normal'
    randomise()
    buildtrack()

def midi():

    rhythm_randomise_button['state'] = 'disabled'
    rhythm_choice_list = [4, 1, 0.5, 0.25]
    rhythm_choice = rhythm_choice_list[var.get()] # either 4, 1, 0.5 or 0.25
    
    global duration_temp
    global half_temp
    
    duration_temp = duration_temp.clear()
    half_temp = half_temp.clear()

    duration_temp = {}
    half_temp = {}
    
    counter = 0
    time = 0
    
    while counter < 4:
        
        duration_temp[time] = rhythm_choice
        half_temp[time] = 1
        
        time += rhythm_choice
        counter += rhythm_choice
            
def randomise():
    
    time = 0

    duration_possible = [0, 0.5, 1]
    half_possible = [1, 2]
    
    duration = random.choice(duration_possible)
    half = random.choice(half_possible)
    
    global duration_temp
    global half_temp
    
    duration_temp = duration_temp.clear()
    half_temp = half_temp.clear()

    duration_temp = {}
    half_temp = {}
    
    while time + max([0.25, duration]) <= 4:
    
        duration_temp[time] = duration
        half_temp[time] = half

        if duration == 0:
            time += random.choice(random.choices([0.25, 0.5], weights = (60,40), k=1))
            
        else:   
            time += max([0.25, duration])
        
        duration = random.choice(duration_possible)
        half = random.choice(half_possible)
        
    buildtrack()
    
def buildtrack():

    global midi_note
    
    global mf
    del mf
    
    global mf_chord
    del mf_chord
    
    global fifth
    global third

    global duration_temp
    global half_temp
    
    #n = bpm_read()
    k = key_read()
    
    mf = MIDIFile(1)
    mf_chord = MIDIFile(1)
    track = 0
    mf.addTrackName(track, 0, 'Sample Track')
    #mf.addTempo(track, 0, n)
    mf_chord.addTrackName(track, 0, 'Sample Track')
    #mf_chord.addTempo(track, 0, n)
    channel = 0
    volume = 100
    
    randomise_time = list(duration_temp.keys()) # time
    randomise_duration = list(duration_temp.values()) # duration
    randomise_half = list(half_temp.values()) # half

    #print(list(duration_temp.keys())) # time
    #print(list(duration_temp.values())) # duration
    #print(list(half_temp.values())) # half
    
    for i in range(len(randomise_time)): # for each timestamp...
        
        if randomise_duration[i] != 0:
            
            mf.addNote(track, channel, midi_note[0]-12+k, randomise_time[i], randomise_duration[i]/randomise_half[i], volume)
            mf.addNote(track, channel, midi_note[1]-12+k, randomise_time[i] + 4, randomise_duration[i]/randomise_half[i], volume)
            mf.addNote(track, channel, midi_note[2]-12+k, randomise_time[i] + 8, randomise_duration[i]/randomise_half[i], volume)
            mf.addNote(track, channel, midi_note[3]-12+k, randomise_time[i] + 12, randomise_duration[i]/randomise_half[i], volume)
    
            mf_chord.addNote(track, channel, midi_note[0]-12+k, randomise_time[i], randomise_duration[i]/randomise_half[i], volume)
            mf_chord.addNote(track, channel, midi_note[1]-12+k, randomise_time[i] + 4, randomise_duration[i]/randomise_half[i], volume)
            mf_chord.addNote(track, channel, midi_note[2]-12+k, randomise_time[i] + 8, randomise_duration[i]/randomise_half[i], volume)
            mf_chord.addNote(track, channel, midi_note[3]-12+k, randomise_time[i] + 12, randomise_duration[i]/randomise_half[i], volume)
            
            #fifth
            
            mf_chord.addNote(track, channel, midi_note[0]-fifth+k, randomise_time[i], randomise_duration[i]/randomise_half[i], volume)
            mf_chord.addNote(track, channel, midi_note[1]-fifth+k, randomise_time[i] + 4, randomise_duration[i]/randomise_half[i], volume)
            mf_chord.addNote(track, channel, midi_note[2]-fifth+k, randomise_time[i] + 8, randomise_duration[i]/randomise_half[i], volume)
            mf_chord.addNote(track, channel, midi_note[3]-fifth+k, randomise_time[i] + 12, randomise_duration[i]/randomise_half[i], volume)  
    
            #third
    
            mf_chord.addNote(track, channel, midi_note[0]-third[0]+k, randomise_time[i], randomise_duration[i]/randomise_half[i], volume)
            mf_chord.addNote(track, channel, midi_note[1]-third[1]+k, randomise_time[i] + 4, randomise_duration[i]/randomise_half[i], volume)
            mf_chord.addNote(track, channel, midi_note[2]-third[2]+k, randomise_time[i] + 8, randomise_duration[i]/randomise_half[i], volume)
            mf_chord.addNote(track, channel, midi_note[3]-third[3]+k, randomise_time[i] + 12, randomise_duration[i]/randomise_half[i], volume)
         
        else:
            continue
               
def export():
    global mf
    global mf_chord
    
    with open('output.mid', 'wb') as outf:
        if var.get() < 4 and var_root.get() == 0:
            mf.writeFile(outf)
        elif var.get() < 4 and var_root.get() == 1:
            mf_chord.writeFile(outf)
        elif var.get() ==4 and var_root.get() == 0:
            mf.writeFile(outf)
        elif var.get() ==4 and var_root.get() == 1:
            mf_chord.writeFile(outf)            

### Tkinter ###

root = tk.Tk()

frame_root = tk.Frame(root)
frame_rhythm = tk.Frame(root)
frame_export = tk.Frame(root)

root.title('Random Chord Progression Generator')
root.geometry('800x700')
root.resizable(False, False)

#ttk.Label(root, text='Random Chord Progression Generator', font=('Arial', 28)).pack()
ttk.Label(frame_root, text='Random Chord Progression Generator', font=('Arial', 20)).grid(row=1, column=1, padx = 160, pady = 10)

# Progression Text
generated = tk.Label(frame_root, text='|  I  |  I  |  I  |  I  |', font=('Arial', 20), relief='raised', width = 20, height = 2, bd = 5)
generated.config(bg='lightblue')
generated.grid(row=2, column=1, pady = 20)


# Generate Progression
button_generate = tk.Button(frame_root, text='Generate Progression', font=('Arial', 16), command=generate)
button_generate.grid(row=3, column=1, pady = 20)

# BPM Scale
bpm_scale = tk.Scale(frame_root, label='BPM', from_=60, to=240, cursor='dot', orient=tk.HORIZONTAL, length=600, tickinterval=10, resolution=1)
bpm_scale.set(120)
bpm_scale.grid(row=4, column=1, pady = 5)

# Key Scale
key_options = ['C / Amin', 'G / Emin', 'D / Bmin', 'A / F#min', 'E / C#min', 'B / G#min', 'F# / Ebmin', 'C# / Bbmin', 'Ab / Fmin', 'Eb / Cmin', 'Bb / Gmin', 'F / Dmin']

key_var = tk.StringVar()
key_var.set('C / Amin')

key_dropdown = tk.OptionMenu(frame_root, key_var, *key_options)
key_dropdown.grid(row=5, column=1, pady = 5)

# Rhythm Choice
pickrhythm = tk.Label(frame_rhythm, text='Pick Your Bassline Rhythm', font=('Arial', 12))
pickrhythm.grid(row=1, column=1, pady = 10, columnspan = 6)

var = tk.IntVar()
rhythm_bar = tk.Radiobutton(frame_rhythm, text='Hold 1 bar', variable=var, value=0, command=midi)
rhythm_bar.select()
rhythm_bar.grid(row=2, column=1, padx = 5, pady = 10)

rhythm_quarter = tk.Radiobutton(frame_rhythm, text='1/4 notes', variable=var, value=1, command=midi)
rhythm_quarter.grid(row=2, column=2, padx = 5, pady = 10)

rhythm_eighth = tk.Radiobutton(frame_rhythm, text='1/8 notes', variable=var, value=2, command=midi)
rhythm_eighth.grid(row=2, column=3, padx = 5, pady = 10)

rhythm_sixteenth = tk.Radiobutton(frame_rhythm, text='1/16 notes', variable=var, value=3, command=midi)
rhythm_sixteenth.grid(row=2, column=4, padx = 5, pady = 10)

rhythm_randomise = tk.Radiobutton(frame_rhythm, text='Randomise', variable=var, value=4, command=generate_rhythm_enable)
rhythm_randomise.grid(row=2, column=5, padx = 5, pady = 10)

rhythm_randomise_button = tk.Button(frame_rhythm, text='Generate Rhythm', state = 'disabled', command=randomise)
rhythm_randomise_button.grid(row=2, column=6, padx = 5, pady = 10)

# Root note vs Chord triad
var_root = tk.IntVar()
rootnote = tk.Radiobutton(frame_export, text='Root Note Only', variable=var_root, value=0)
rootnote.grid(row=1, column=1, padx = 5, pady = 10)

triad = tk.Radiobutton(frame_export, text='Chord/Triad', variable=var_root, value=1)
triad.grid(row=1, column=2, padx = 5, pady = 10)

# Play
button_play = tk.Button(frame_export, text='Play', font=('Arial', 10), command=play)
button_play.grid(row=2, column=1, columnspan = 6, pady = 20)

# Export MIDI
button_midi = tk.Button(frame_export, text='Export MIDI', font=('Arial', 10), command=export)
button_midi.grid(row=3, column=1, columnspan = 6, pady = 10)

frame_root.grid()
frame_rhythm.grid()
frame_export.grid()
root.mainloop()




