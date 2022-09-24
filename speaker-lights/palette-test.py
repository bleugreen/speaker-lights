from screen import Screen
from palette import Palette
from analyzer import Analyzer
from smoothList import SmoothList
import cairo
import time
import os
from localdb import LocalDB

screen = Screen()
palette = Palette(['red', 'red'])
pid = ''
db = LocalDB()

def updatePalette():
    global palette, pid
    plist = db.get_current_cover()
    if plist:
        if len(plist) != len(palette.palette):
            print(plist)
            palette = Palette(plist)
            return True



def main():
    prevTime = time.time()
    framecount = 0
    prevFramecount=0
    while(True):
        ctx = screen.getCtx()

        plen = len(palette.palette)
        h = 15.0/plen
        y=0
        for i in range(plen):
            r,g,b = palette.palette[i].rgb
            ctx.set_source_rgb(r,g,b)
            ctx.rectangle(0, y, 34, h)
            ctx.fill()
            y += h


        screen.update()
        time.sleep(0.1)

        t = time.time()
        framecount +=1
        if t - prevTime >= 1:
            print('frames: ',(framecount-prevFramecount))
            updatePalette()
            prevTime = t
            prevFramecount=framecount

main()
