import pyaudio
import time
import numpy as np
import audioop
import essentia
from essentia.standard import *

class Analyzer:
    CHUNK = 1024
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 44100
    
    def __init__(self):
        self.fulldata = np.array([])
        self.barkbands = np.array([])
        self.loud = 0.0
        self.maxloud = 0.0
        
        self.onset = 0.0
        self.lowonset = 0.0
        self.lowonsetraw = 0.0
        self.onsetmax = 0.1
        
        self.meanVol = 0.0
        self.volLength = 20.0
        self.silent = False
        
        self.toggles = {'bark':False, 'bass':False}
        
        self.w = Windowing(type='hann')
        self.lowpass = LowPass(cutoffFrequency=120)
        self.onsetdetection = Leq()
        self.spectrum = Spectrum()
        self.bark = BarkBands()
        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=Analyzer.FORMAT,
                    channels=Analyzer.CHANNELS,
                    rate=Analyzer.RATE,
                    input=True,
                    frames_per_buffer=Analyzer.CHUNK,
                    stream_callback=self.audioIn)

    def audioIn(self, in_data, frame_count, time_info, flag):
        audio_data = np.frombuffer(in_data, dtype=np.single)
        
        self.onset = -1*self.onsetdetection(audio_data)
        
        self.meanVol -= self.meanVol/self.volLength
        self.meanVol += self.onset/self.volLength
        
        if self.onset > 70:
            self.silent = True
        else:
            self.silent = False
        
        #no need to run analysis if nothing is playing
        if not self.silent:
            spec = self.spectrum(self.w(audio_data))
            self.barkbands = self.bark(spec)
            self.lowonset =-1*self.onsetdetection(self.lowpass(audio_data))
            if self.lowonset > self.onsetmax:
                self.onsetmax = self.lowonset
            else:
                self.lowonset = self.onsetmax - self.lowonset
            self.lowonset = self.lowonset / self.onsetmax

    #        self.loud = self.loudness(audio_data)
    #        if self.loud > self.maxloud:
    #            self.maxloud -= self.maxloud/20
    #            self.maxloud += self.loud / 20
    #        self.loud = self.loud / self.maxloud
            self.rms = audioop.rms(audio_data, 2)

        return (audio_data, pyaudio.paContinue)

    
    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        
    def get_bark(self):
        return self.barkbands
        
    def get_rms(self):
        return self.rmsval
    
    def get(self, name=''):
        if name == 'silent':
            return self.silent
        elif name == 'bark':
            return self.barkbands
        elif name == 'bass':
            return self.lowonset
        else:
            return self.lowonset, self.barkbands, self.silent
