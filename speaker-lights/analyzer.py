import pyaudio
import time
import numpy as np
import audioop
import librosa

class Analyzer:
    
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        
        self.fulldata = np.array([])
        self.rms = 1
        self.max_rms = 1
        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    frames_per_buffer=self.CHUNK,
                    stream_callback=self.callback)

    def callback(self, in_data, frame_count, time_info, flag):
        audio_data = np.frombuffer(in_data, dtype=np.int16)

        self.rms = audioop.rms(audio_data, 2)
        if self.rms > self.max_rms:
            self.max_rms = self.rms

        self.fulldata = audio_data
        return (audio_data, pyaudio.paContinue)

    
    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        
    def get_rms_ratio(self):
        return float(self.rms) / self.max_rms
    
    def get_fulldata(self):
        return self.fulldata
