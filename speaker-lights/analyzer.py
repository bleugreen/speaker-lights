import pyaudio
import time
import numpy as np
import audioop

class Analyzer:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    
    def __init__(self):
        self.fulldata = np.array([])
        self.rms = 1
        self.max_rms = 1
        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=Analyzer.FORMAT,
                    channels=Analyzer.CHANNELS,
                    rate=Analyzer.RATE,
                    input=True,
                    frames_per_buffer=Analyzer.CHUNK,
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
