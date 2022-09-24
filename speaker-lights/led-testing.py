from screen import Screen
from palette import Palette
from analyzer import Analyzer
from smoothList import SmoothList
import time
import os
from localdb import LocalDB

db = LocalDB()
screen = Screen()
analyzer = Analyzer(numBarkBands=27)
palette = Palette(['red', 'red'])
pid = ''
pitch = 0
hfcMax = 0.1
mfccLen = 40
mfccBands = SmoothList(length=mfccLen, ceilDecay=0.9999, meanFrames=2)

def bassBar(ctx, data):
    bassLen = data.len() / 5
    bass = 0
    for i in range(round(bassLen)):
        bass += data.get(i)
    bass = bass / bassLen
    wB = bass*7
    br = (bass)*(bass)
    marginB = (7-wB)/2
    # r,g,b = 1,1,1
    r,g,b = palette.getColor(br)
    ctx.set_source_rgba(r,g,b,br)
    ctx.rectangle(5+marginB, 14, wB, 1)
    ctx.rectangle(22+marginB, 14, wB, 1)
    ctx.fill()

def spectrum(ctx, data):
    global palette
    scaleLen = data.len()
    for i in range(scaleLen):
        val = data.get(i)
        r,g,b = palette.getColor(float(i)/scaleLen)

        w = val*7
        margin = (7-w)
        h = (i/scaleLen)*15
        h0 = 15.0-h
        br = (r+g+b)/(3*255.)
        br = (val+(br*3))/4.0

        ctx.set_source_rgba(r,g,b, br)

        ctx.rectangle(5, h, w/2, 15.0/scaleLen)
        ctx.rectangle(5+margin+w/2, h, w/2, 15.0/scaleLen)
        ctx.rectangle(5, h0, w/2, 15.0/scaleLen)
        ctx.rectangle(5+margin+w/2, h0, w/2, 7.5/scaleLen)
        ctx.fill()
        ctx.rectangle(22, h, w/2, 15.0/scaleLen)
        ctx.rectangle(22+margin+w/2, h, w/2, 7.5/scaleLen)
        ctx.rectangle(22, h0, w/2, 15.0/scaleLen)
        ctx.rectangle(22+margin+w/2, h0, w/2, 7.5/scaleLen)
        ctx.fill()




def onsetRect(onset, ctx):
    h = onset*15
    r,g,b = palette.getColor(pitch/12.0)
    br = (r+g+b)/(3*255.)
    ctx.set_source_rgba(r,g,b, (br+onset)/2.0)
    ctx.rectangle(0, 0, 1, h)
    ctx.rectangle(16, 0, 1, h)
    ctx.rectangle(17, 0, 1, h)
    ctx.rectangle(33, 0, 1, h)
    ctx.fill()

def hfcRect(hfc, ctx):
    global palette
    h = hfc*12
    r,g,b = palette.getColor(pitch/12.0)
    br = (r+g+b)/(3*255.)
    br = (br+hfc)/2.0
    ctx.set_source_rgb(r,g,b)
    ctx.rectangle(4, 0, 1, h)
    ctx.rectangle(12, 0, 1, h)
    ctx.rectangle(13, 0, 1, h)
    ctx.rectangle(29, 0, 1, h)
    ctx.fill()



def pitchBars(ctx, maxIdx):
    global palette
    r,g,b = palette.getColor(pitch/12.0)
    br = mfccBands.get(mfccBands.maxIdx)
    ctx.set_source_rgba(r,g,b, br)
    ctx.rectangle(0, pitch, 5, 2)
    ctx.rectangle(12, pitch, 5, 1.5)
    ctx.rectangle(17, pitch, 5, 1.5)
    ctx.rectangle(29, pitch, 5, 1.5)
    ctx.fill()

def updatePalette():
    global palette, pid, hfcMax
    curr_pid = db.get_current()
    if curr_pid != pid:
        pid = curr_pid
        for i in range(len(mfccBands.max)):
            mfccBands.max[i] = mfccBands.max[i]*0.5
        hfcMax = hfcMax*0.8

    plist = db.get_current_cover()
    if plist:
        if len(plist) != len(palette.palette):
            print(plist)
            palette = Palette(plist)
            return True





def main():
    global maxOnset, hfcMax

    prevTime = time.time()
    framecount = 0
    prevHfc = 0
    prevFramecount=0
    hfcMean = 100
    while(True):
        hpcp = analyzer.get('hpcp')
        updatePitch(hpcp)

        ctx = screen.getCtx()

        bassBar(ctx, mfccBands)
        pitchBars(ctx, mfccBands.maxIdx)

        rhfc = analyzer.get('hfc')
        hfc =max(rhfc-prevHfc, 0)
        prevHfc =rhfc

        if hfc > hfcMax:
            hfcMax = hfc
        hfcMean = ((70*hfcMean)+(5*hfcMax)+(25*hfc))/100.
        mfccBands.update(analyzer.get('mel'))
        spectrum(ctx, mfccBands)

        if hfc > hfcMean*0.9:
            hfcRect(hfc/hfcMean, ctx)

        rawOnset = analyzer.get('onset')
        if rawOnset > maxOnset:
            maxOnset  = rawOnset
        onset = rawOnset / maxOnset
        onsetRect(onset, ctx)


        screen.update()
        updatePalette()
        t = time.time()
        framecount +=1
        if t - prevTime >= 1:
            print('frames: ',(framecount-prevFramecount))

            prevTime = t
            prevFramecount=framecount



def updatePitch(hpcp):
    global pitch
    i = 0
    for w in hpcp:
        if w >=1:
            pitch = (pitch*10+i)/11.0
        i+=1
main()
