import mido
import os
import numpy as np
from scipy.io.wavfile import write as writewav
from intruments import *
from effects import *
from effects import *
import sys


def initFunc():
    current_dir = os.getcwd()  # Get the current directory path

    sounds_dir = os.path.join(current_dir, 'sounds')  # Create the path to the 'sounds' folder

    if not os.path.exists(sounds_dir):  # Check if the 'sounds' folder exists
        os.mkdir(sounds_dir)

    if not os.path.isfile(os.path.join(sounds_dir, 'clarinet_notes.npy')):  # Check if the file exists
        create_clarinet_notes()

    if  not os.path.isfile(os.path.join(sounds_dir, 'guitar_notes.npy')):  # Check if the file exists
        create_guitar_notes()

    if  not os.path.isfile(os.path.join(sounds_dir, 'tomtom_notes.npy')):  # Check if the file exists
        create_tomtom_notes()
    
    if  not os.path.isfile(os.path.join(sounds_dir, 'snare_notes.npy')):  # Check if the file exists
        create_snare_notes()



def pickUpTrackInfo(filename):
  mid = mido.MidiFile(filename)
  ticks_per_beat = mid.ticks_per_beat
  tempo = 0
  trackInfo = []

  for trackindex, track in enumerate(mid.tracks):

    times = []
    notes = []

    #creamos una lista con los tiempos absolutos de los mensajes del track

    for i, msg in enumerate(track):
      if msg.type == 'set_tempo':
        tempo = msg.tempo
      if times!= []:  
        times.append(times[-1]+msg.time)
      else:
        times.append(msg.time)

    times = [mido.tick2second(x, ticks_per_beat, tempo) for x in times] 

    #buscamos la duracion de cada nota del track

    for i, msg in enumerate(track):  

        if msg.type!='note_on' or msg.velocity==0:
            continue

        note = msg.note
        abs_time = times[i]
        duration = 0

        for j, msg2 in enumerate(track[i+1:]):
            if msg2.type=='note_off' and msg2.note==note:
                duration = times[j+i+1]-times[i]
                break
            elif msg2.type=='note_on' and msg2.note==note and msg2.velocity==0:
                duration = times[j+i+1]-times[i]
                break

        notes.append([abs_time, duration, note])

    trackInfo.append([trackindex, track.name, notes])

  return trackInfo

def synthesizeSong(tracks, trackespecifications, outname):
    print("I'm synthesizing")

    file_len = flen(tracks)  
    samplerate = 44100
    data = np.zeros(int(np.ceil(file_len)*samplerate))    


    for i, track in enumerate(tracks):

        specs = next((d for d in trackespecifications if d.get('index') == i), None)

        if specs == None or not (specs["volume"] > 0):
            continue #me salteo el track

        instrument_mapping = {
            'acoustic guitar': guitar2,
            'clarinet': clarinet2,
            'tom': tomtom2,
            'snare drum': snaredrum2,
            'flute': flute2,
            'saxo': saxo2,
            'piano': piano2,
            'electric piano': electricpiano2,
            'viola': viola2,
            'violin': violin2,
            'cello': cello2,
            'hotbath': hotbath2,
            'string ensemble': string_ensemble2
        }

        track_intrument = specs['instrument']
        instrfunc = instrument_mapping.get(track_intrument)

        base_track_arr = np.zeros(int(np.ceil(file_len)*samplerate))
        noteQuant = len(track[2])

        currentNoteNumber = 1 #for printing purposes
        print('')#for printing purposes
        for note in track[2]:
            
            print(str(currentNoteNumber), '/'+ str(noteQuant)+'- track: '+ 
            str(specs['index']) + ' ' + specs['instrument'])#for printing purposes
            sys.stdout.write("\033[F") # Cursor up one line
            currentNoteNumber += 1#for printing purposes

            abs_time = note[0] #time when the note strats playing (s)
            duration = note[1] #duration of the note (s)
            pitch = note[2] #pitch of the note in midi values

            if not (duration>0):
                continue #if the note has no duration we don't add anything to the track

            instrument_note = instrfunc(pitch, duration, samplerate)
            instrument_note2 = instrument_note/np.max(np.abs(instrument_note))
            offset = int((abs_time)*samplerate)
            
            for i, data in enumerate(instrument_note2):
                base_track_arr[offset+i] = data


        if specs["echo"] and specs["echoval"]==1:
            base_track_arr=echo(base_track_arr)
        if specs["echo"] and specs["echoval"]==2:
            base_track_arr=echo2(base_track_arr)
        if specs["flanger"]:
            base_track_arr=flanger(base_track_arr)
        if specs["wahwah"]:
            base_track_arr=wahwah(base_track_arr)

        track_volume = specs["volume"]
        data += base_track_arr*track_volume/100 #we scale the track by track volume and add it to main audio array

    norm_data = np.int16(data / np.max(np.abs(data)) * 32767)

    if outname == '': outname = 'output.wav'
    elif len(outname)<5 or outname[-4:] != '.wav':
        outname +='.wav'

    writewav(outname, 44100, norm_data)

    print('')
    print('finished!')                      
     

def flen(trackInfo):
    file_length=0
    for track in trackInfo:
        if len(track[2]) != 0:
            last_note = track[2][-1]
            track_len = last_note[0]+last_note[1]
            if track_len > file_length:
                file_length=track_len

    return file_length+5



