from screen import Screen
from palette import Palette
from analyzer import Analyzer
from smoothList import SmoothList
import time
import os
from localdb import LocalDB
from stringsim import String
import random

db = LocalDB()
screen = Screen()
analyzer = Analyzer(numBarkBands=27)
palette = Palette(['red', 'red'])
pid = ''
mfccLen = 40
mfccBands = SmoothList(length=mfccLen, ceilDecay=0.9999, meanFrames=2)
strings_right = []
strings_left= []
for i in range(10):
    strings_right.append(String(nodes=15, center=25, color='blue'))
    strings_left.append(String(nodes=15, center=9, color='blue'))

def updatePalette():
    global palette, pid, hfcMax, strings_right
    curr_pid = db.get_current()
    if curr_pid != pid:
        pid = curr_pid
        # when a new song is detected, scale down the maxes so it comes in 'loud'
        for i in range(len(mfccBands.max)):
            mfccBands.max[i] = mfccBands.max[i]*0.5
        hfcMax = hfcMax*0.8

    plist = db.get_current_cover()
    if plist:
        if len(plist) != len(palette.palette):
            print(plist)
            palette = Palette(plist)
            for i in range(len(strings_right)):
                color = palette.getColor(float(i)/len(strings_right))
                strings_right[i].color = color
                strings_left[i].color = color
            return True

def main():
    prevTime = time.time()
    framecount = 0
    prevFramecount=0
    while(True):
        # get the drawing surface
        ctx = screen.getCtx()
        # get the newest audio data
        mfccBands.update(analyzer.get('mel'))
        # sum the 40 mfcc bands into 10 string 'pulses'
        for i in range(10):
            val = 0
            for j in range(i*4, i*4+4):
                val += mfccBands.get(j)
            val = val*10
            # if it passes the threshold, push it the other way
            # also make even strings go the other way
            if val > 20 or val < -20 or i%2 == 0:
                val = -val
            # strings were moving slow, so now they update twice per frame
            strings_right[i].update(val, i+1)
            strings_right[i].update(val , i+1)
            strings_left[i].update(val, i+1)
            strings_left[i].update(val , i+1)

            color = palette.getColor(float(i)/10.0)
            strings_right[i].draw(ctx, color)
            strings_left[i].draw(ctx, color)

        screen.update()
        updatePalette()

        t = time.time()
        framecount +=1
        if t - prevTime >= 1:
            print('frames: ',(framecount-prevFramecount))
            prevTime = t
            prevFramecount=framecount

main()
