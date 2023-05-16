import mido
import numpy as np
import librosa
import scipy.io.wavfile as wavfile
from scipy.signal import butter, filtfilt, resample
from scipy.fft import fft, ifft
import pytsmod as tsm


#create clarinet notes if they do not exist yet

def create_clarinet_notes():
    clarinet_notes = np.zeros((129,44100*5))

    for midi_note in range(129):
        f = 440*2**((midi_note-69)/12)
        clarinet_notes[midi_note] = clarinet(f, 5, 44100)

    np.save('./sounds/clarinet_notes.npy', clarinet_notes)

def clarinet(f, time, samplerate):

  y2 = np.load('y2.npy')
  t = np.linspace(0,time, int(samplerate*time))

  It = np.interp(t, np.linspace(0,time,44100),y2)
  sample = np.cos(argfunc(t, It, 1, f*2, f*3))
  return sample

def argfunc(t,It, At,fc,fm):
    return np.pi*fc*t+It*np.cos(2*np.pi*fm*t-np.pi/2)-np.pi/2

#play clarinet note

clar_notes = None
first_call_clar = True

def clarinet2(midi_note, duration, sr):
    global clar_notes
    global first_call_clar
    if first_call_clar == True:
        clar_notes = np.load('./sounds/clarinet_notes.npy')
        first_call_clar = False

    note = clar_notes[midi_note][:int((duration+0.05)*44100)]
    envelope = generate_envelope(note.size, sustain_level=0.95)
    
    return envelope*note

#create guitar notes if they do not exist yet

def create_guitar_notes():
    guitar_notes = np.zeros((129,44100*3))

    for midi_note in range(129):
        f = 440*2**((midi_note-69)/12)
        note = guitar(f, 3, 44100)
        guitar_notes[midi_note] = note

    np.save('./sounds/guitar_notes.npy', guitar_notes)

def guitar(f, time, samplerate):
    note =  guitar_raw(f, 3, 20000)
    return librosa.resample(note, orig_sr = 20000, target_sr=44100)
  
def guitar_raw(note_freq, n=3, samplerate=44100): 
  p = int((samplerate/note_freq)-1/2) 
  #print(p)
  #print(samplerate/(p+1/2))
  t = np.linspace(0,4, samplerate*n)

  y = np.zeros(samplerate*n)

  for i in range(p):
    A = 1*np.random.choice([-1,1]) #for -p<=t<=0
    y[i] = A*np.sin((2*np.pi/p)*i)

  for i in range(p,samplerate*n):
    #Notas graves
    if note_freq < 200:
      m=0.98
    else:
      m=1
      
    if i-p-2>0:
      y[i] = (y[i-p] + y[i-p-1] +y[i-p-2])*m/3
    elif i-p-1>0:
      y[i] = (y[i-p] + y[i-p-1])/3
    else:
      y[i] = (y[i-p])/3
    
  return y
#play guitar note

guitar_notes=None
first_call_guit = True
def guitar2(midi_note, dur, sr):
    global guitar_notes
    global first_call_guit
    if first_call_guit == True:
        guitar_notes = np.load('./sounds/guitar_notes.npy')
        first_call_guit = False
    return guitar_notes[midi_note]

first_call_snare = True
snare_notes = None

def snaredrum2(note, time, samplerate):
    global first_call_snare, snare_notes
    if first_call_snare:
        snare_notes = np.load('./sounds/snare_notes.npy')
        first_call_snare = False
    return snare_notes
    

def snaredrum(note, time, samplerate):
  drumnote = drums_notes(200, samplerate)
  return librosa.resample(drumnote, orig_sr = 20000, target_sr=44100)


def create_snare_notes():
    note = snaredrum(0,0,44100)
    np.save('./sounds/snare_notes.npy', note)

first_call_tomtom = True
tomtom_notes = None

def tomtom2(note, time, samplerate):
    global first_call_tomtom, tomtom_notes
    if first_call_tomtom:
        tomtom_notes = np.load('./sounds/tomtom_notes.npy')
        first_call_tomtom = False

    return tomtom_notes


def tomtom(note, time, samplerate):
  drumnote = drums_notes(20, samplerate)
  return librosa.resample(drumnote, orig_sr = 20000, target_sr=44100)

def create_tomtom_notes():
    note = tomtom(0,0,44100)
    np.save('./sounds/tomtom_notes.npy', note)



def drums_notes(note_freq, samplerate):
  #p around 200 snare drum
  #p around 20 brushed tom-tom

  
  samplerate = 20000
  p = int((samplerate/note_freq)-1/2)  
  t = np.linspace(0,4, samplerate*1)

  y = np.zeros(samplerate*1)
  b = 0.5
  #Increasing S increases the snare sound, allowing smaller values of p 
  S = p*0.15
  #print(S)

  for i in range(p):
    A = 10 #10*np.random.choice([-1,1]) #for -p<=t<=0
    y[i] = A*np.sin((2*np.pi/p)*i)

  for i in range(p,samplerate*1):
    B = np.random.choice([1, -1, 1/2, -1/2], 1, p=[b*(1-1/S), (1-b)*(1-1/S), b/S, (1-b)/S])
    #print(b)
    if abs(B) == 1:
      y[i] = B*y[i-p]
    else:
      y[i] = B*(y[i-p]+y[i-p-1])

  return y


def flute2(note, duration, sr):
    freq = 440*2**((note-69)/12)
    note = flute(freq, duration+0.05, 44100)
    return note


def flute(freq, duration, sr=44100):
    filename = './sounds/samples/fluteC6.npy'
    note = changepitch(freq, 1046.50, filename, notelen=duration) 
    envelope = generate_envelope(note.size, sustain_level=0.99)
    return note*envelope
    
def saxo2(note, duration, sr):
    freq = 440*2**((note-69)/12)
    note = saxo('DO', freq, duration+0.05, 44100)
    envelope = generate_envelope(note.size)

    return note


def saxo(note, freq, duration, sr=44100):
    
    filename = './sounds/samples/saxoC4.npy'
    note = changepitch(freq, 261.63, filename, notelen=duration) 
    return note
    


def electricpiano2(note, duration, sr):
    freq = 440*2**((note-69)/12)
    note = electricpiano(freq, duration, 44100)
    envelope = generate_envelope(note.size)
    return note*envelope

def electricpiano(freq, duration, sr=44100):
    filename = './sounds/samples/electricpianoC3.npy' 
    return changepitch(freq, 130.813, filename, notelen=duration) 
   

def electricpiano2(note, duration, sr):
    freq = 440*2**((note-69)/12)
    note = electricpiano(freq, duration, 44100)
    return note

def piano2(note, duration, sr):
    freq = 440*2**((note-69)/12) 
    return piano(freq, duration, 44100)

def piano(freq, duration, sr=44100):
    

    if freq>523:
        filename = './sounds/samples/pianoC6.npy'
        basefreq = 1046.50
    elif freq>160:
        filename = './sounds/samples/pianoC4.npy'
        basefreq = 261.63
    else:
        filename = './sounds/samples/pianoC2.npy'
        basefreq = 65.41


    return changepitch(freq, basefreq, filename, rel_dur = 0.5)

def violin(freq, duration, sr=44100):

    filename = './sounds/samples/violinC4.npy'
    note = changepitch(freq, 261.63, filename, notelen=duration) 
    return note

def violin2(note, duration, sr):
    freq = 440*2**((note-69)/12)
    note = violin(freq, duration, 44100)
    return note

def viola(freq, duration, sr=44100):
    
    filename = './sounds/samples/violaC5.npy'
    note = changepitch(freq, 523.25, filename, notelen=duration) 
    return note

def viola2(note, duration, sr):
    freq = 440*2**((note-69)/12)
    note = viola(freq, duration, 44100)

    return note

def cello(freq, duration, sr=44100):
    
    if freq<130.81:
        filename = './sounds/samples/celloC2.npy'
        note = changepitch(freq, 65.41, filename, notelen=duration) 
    else:
        filename = './sounds/samples/celloC4.npy'
        note = changepitch(freq, 261.63, filename, notelen=duration) 
    
    return note

def cello2(note, duration, sr):
    freq = 440*2**((note-69)/12)
    note = cello(freq, duration, 44100)

    return note

def string_ensemble(freq, duration, sr=44100):
    
    filename = './sounds/samples/stringensembleC4.npy'
    note = changepitch(freq, 261.63, filename, notelen=duration) 
    return note

def string_ensemble2(note, duration, sr):
    freq = 440*2**((note-69)/12)
    note = string_ensemble(freq, duration, 44100)

    return note

def hotbath(freq, duration, sr=44100):
    
    filename = './sounds/samples/hotbathC2.npy'
    note = changepitch(freq, 65.41, filename, notelen=duration) 
    return note

def hotbath2(note, duration, sr):
    freq = 440*2**((note-69)/12)
    note = hotbath(freq, duration, 44100)

    return note

def generate_envelope(note_duration, attack_duration=int(0.05*44100), decay_duration=int(0.05*44100), sustain_level=0.8, release_duration=int(0.05*44100)):
    total_duration = note_duration
    if total_duration < (attack_duration + release_duration+decay_duration):
        # Adjust the durations if the total duration is too short
        attack_duration = total_duration / 3
        decay_duration = total_duration / 3
        release_duration = total_duration / 3

    envelope = np.zeros(total_duration)

    attack_samples = int(attack_duration)
    decay_samples = int(decay_duration)
    sustain_samples = total_duration - attack_samples - decay_samples - int(release_duration)

    # Attack stage
    attack = np.linspace(0, 1, attack_samples)
    envelope[:attack_samples] = attack

    # Decay stage
    decay = np.linspace(1, sustain_level, decay_samples)
    envelope[attack_samples:attack_samples + decay_samples] = decay

    # Sustain stage
    envelope[attack_samples + decay_samples:attack_samples + decay_samples + sustain_samples] = sustain_level

    # Release stage
    release = np.linspace(sustain_level, 0, int(release_duration))
    envelope[-len(release):] = release

    return envelope

def changepitch(targetf, sourcef, filename, notelen=-1.0, rel_dur=0):
    sample = np.load(filename)
    originalLen = sample.size/44100
    if notelen<0:
        notelen=originalLen
    if rel_dur >0:
        notelen=originalLen*rel_dur
    ratio = sourcef/targetf
    sample = librosa.resample(sample,orig_sr = 44100,target_sr = int(44100*ratio))
    new_sample = tsm.wsola(sample, 1/(ratio))
    if notelen<originalLen:
        new_sample = new_sample[:int(notelen*44100)]
    else:
        new_sample = tsm.wsola(new_sample, notelen/originalLen)
    return new_sample
