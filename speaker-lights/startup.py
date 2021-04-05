#!/usr/bin/python3

# Screen wrapper to allow drawing to LED strip as 2D cairo ImageSurface

import board
import random
import adafruit_dotstar as dotstar
from colour import Color
import math
import numpy as np
import time

numpixels = 247           #
order     = dotstar.BGR  #

star_map = np.array([[8,10,15,17,19,21,4,6],
                     [7,9,14,16,18,20,3,5],
                     [13,2,-1,-1,-1,-1,-1,-1],
                     [12,1,-1,-1,-1,-1,-1,-1],
                     [0,11,-1,-1,-1,-1,-1,-1,]])

strip     = dotstar.DotStar(board.SCK, board.MOSI, numpixels,
                  brightness=0.9, auto_write=False, pixel_order=order)

b = [0,0,0,0,0]
for t in range(101):
    if t < 20:
        b[0] = (t*5)
    elif t<40:
        b[0] = 100-((t-20)*5)
        b[1] = (t-20)*5
    elif t<60:
        b[0] = 0
        b[1] = 100-((t-40)*5)
        b[2] = (t-40)*5
    elif t<75:
        b[1] = 0
        b[2] = 100-((t-60)*5)
        b[3] = (t-60)*5
    elif t<80:
        b[2] = 100-((t-60)*5)
        b[3] = 100-((t-75)*6)
        b[4] = (t-75)*5
    elif t<90:
        b[2] = 0
        b[3] = 100-((t-75)*6)
        b[4] = (t-75)*5
    elif t<100:
        b[3] = 0
        b[4] = 100-(t-90)*10
    else:
        b = [0,0,0,0,0]
    
    for i in range(len(star_map)):
        for x in star_map[i]:
            if x > 0:
                if i==0:
                    strip[x] = (b[i],0,0)
                elif i==1:
                    strip[x] = (int(b[i]/2),b[i],0)
                elif i==2:
                    strip[x] = (0,b[i],0)
                elif i==3:
                    strip[x] = (0,int(b[i]/2),b[i])
                else:
                    strip[x] = (0,0,b[i])
    strip.show()
    time.sleep(1/100.0)
for i in strip:
    i = 0
strip.show()

    
