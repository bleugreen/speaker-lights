import audioop
import time

import essentia.standard as est
import numpy as np
import pyaudio
# from essentia.standard import *


class Analyzer:
    CHUNK = 1024
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 44100

    analyzer = 'placeholder'

    def __init__(self, numBarkBands=27):
        self.fulldata = np.array([])

        self.barkbands = np.array([])
        self.hpcp = np.array([])
        self.chroma = np.array([])
        self.mfccBands = np.array([])
        self.loud = 0.0
        self.maxloud = 0.0
        self.tempoTicks =0
        self.flatness = 0

        self.onset = 0.0
        self.lowonset = 0.0
        self.lowonsetraw = 0.0
        self.onsetmax = 0.1

        self.rms= 0.0

        self.meanVol = 0.0
        self.volLength = 20.0
        self.silent = False

        self.toggles = {'bark':False, 'bass':False}

        self.loudness = 0.0
        self.loudDetector = est.Loudness()

        self.w = est.Windowing(type='hann')
        self.lowpass = est.LowPass(cutoffFrequency=120)
        self.onsetDet = est.OnsetDetection()
        self.spectrum = est.Spectrum()
        self.bark = est.BarkBands(numberBands=numBarkBands)
        self.hfcDet = est.HFC()
        self.hfc = 0

        self.melDet = est.MelBands(numberBands=numBarkBands, highFrequencyBound=10000)

        self.specPeaks = est.SpectralPeaks()
        self.HPCPDet = est.HPCP()

        self.mfccDet = est.MFCC(inputSize=513, numberBands=40)

        # self.freqBander = FrequencyBands()
        # self.noveltyCurve = NoveltyCurve()

        self.flatDet = est.Flatness()

        # self.chordDet = ChordsDetection()
        # self.chordData = ''

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=Analyzer.FORMAT,
                    channels=Analyzer.CHANNELS,
                    rate=Analyzer.RATE,
                    input=True,
                    frames_per_buffer=Analyzer.CHUNK,
                    stream_callback=self.audioIn)
        self.maxrms = 1.0

    def audioIn(self, in_data, frame_count, time_info, flag):
        audio_data = np.frombuffer(in_data, dtype=np.single)

        spec = self.spectrum(self.w(audio_data))

        self.loudness = self.loudDetector(audio_data)

        self.hfc = self.hfcDet(spec)

        self.mfccBands, mfccCoeff = self.mfccDet(spec)

        [freqs, mags1] = self.specPeaks(spec)
        self.hpcp = self.HPCPDet(freqs, mags1)

        self.onset = self.onsetDet(spec, [])

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
        elif name == 'onset':
            return self.onset
        elif name == 'hfc':
            return self.hfc
        elif name == 'loudness':
            return self.loudness
        # elif name == 'chord':
        #     return self.chordData
        elif name == 'hpcp':
            return self.hpcp
        # elif name == 'chroma':
        #     return self.chroma
        elif name == 'mel':
            return self.mfccBands
        elif name == 'flatness':
            return self.flatness
        else:
            return self.lowonset, self.barkbands, self.silent
