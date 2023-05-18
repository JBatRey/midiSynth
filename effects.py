import numpy as np
import scipy.signal as signal
import librosa

# echo

def echo(track, delay_time= 500, decay_factor= 0.5):
    '''delay_time  #  milisegundos de delay
        decay_factor # cuanto le matas la amplitud al eco, deberia ser editable en GUI
    '''
    
    delay_samples = int(delay_time * 44100 / 1000)
    echo_y = np.concatenate((np.zeros(delay_samples),track))
    ret = echo_y[:-delay_samples]*decay_factor + track   # decay
    return ret

def echo2(track, delay_time= 250, decay_factor= 0.5):
    '''delay_time  #  milisegundos de delay
        decay_factor # cuanto le matas la amplitud al eco, deberia ser editable en GUI
    '''
    
    delay_samples = int(delay_time * 44100 / 1000)
    echo_y = np.concatenate((np.zeros(delay_samples),track))
    echo_y2 = np.concatenate((np.zeros(2*delay_samples),track))
    ret = echo_y2[:-delay_samples*2]*decay_factor*0.5 + track   # decay
    ret += echo_y[:-delay_samples]*decay_factor + track   # decay
    return ret

def flanger(input_signal, maxdelay = 10, fflanger = 0.95, gain = 0.5):

    # maxdelay (< 15ms)
    # fflanger (~ 1Hz)
    # gain (number betweeen 0 and 1)

    num = int(maxdelay * 1e-3 * 44100)
    output_signal = np.zeros(len(input_signal))
    for n in range(len(input_signal)):
        d = int(0.5 * num * (1 + np.sin(2 * np.pi * fflanger * n / 44100)))
        if d < n:
            output_signal[n] = input_signal[n] + gain * input_signal[n-d]
        else:
            output_signal[n] = input_signal[n] 

    return output_signal

def wahwah(input_signal, damp= 0.2, wahf = 2000):

    minf = wahf/2
    maxf = wahf*2

    # damp wahwah damping factor (< 0.5)
    # minf minimum center cutoff frequency (~ 500Hz)
    # maxf maximum center cutoff frequency (~ 5000Hz)
    # wahf "wah" frequency (~ 2000Hz)

    output_signal = np.zeros(len(input_signal))
    outh = np.zeros(len(input_signal))
    outl = np.zeros(len(input_signal))
    delta = wahf / 44100
    centerf = np.concatenate((np.arange(minf, maxf, delta), np.arange(maxf, minf, -delta)))
    while len(centerf) < len(input_signal):
        centerf = np.concatenate((centerf, centerf))
    centerf = centerf[:len(input_signal)]
    f1 = 2 * np.sin(np.pi * centerf[0] / 44100)
    outh[0] = input_signal[0]
    output_signal[0] = f1 * outh[0]
    outl[0] = f1 * output_signal[0]
    for n in range(1, len(input_signal)):
        outh[n] = input_signal[n] - outl[n-1] -  2 * damp * output_signal[n-1]
        output_signal[n] = f1 * outh[n] + output_signal[n-1]
        outl[n] = f1 * output_signal[n] + outl[n-1]
        f1 = 2 * np.sin(np.pi * centerf[n] / 44100)
    return output_signal