#!/usr/bin/python3

# Simple strand test for Adafruit Dot Star RGB LED strip.
# This is a basic diagnostic tool, NOT a graphics demo...helps confirm
# correct wiring and tests each pixel's ability to display red, green
# and blue and to forward data down the line.  By limiting the number
# and color of LEDs, it's reasonably safe to power a couple meters off
# USB.  DON'T try that with other code!

import time
import board
import adafruit_dotstar as dotstar
from colour import Color
import math
from rings import Ring

numpixels = 300           # Number of LEDs in strip
order     = dotstar.BGR  # Might need GRB instead for older DotStar LEDs
strip     = dotstar.DotStar(board.SCK, board.MOSI, numpixels,
              brightness=0.5, auto_write=False, pixel_order=order)
ring = Ring(strip)

def spinFan():
    radius = 3
    width = 0
    grow = True
    angle = 0
    spin = 0
    while True:
        ring.fan(angle, width, 0x020022)
        ring.arc(-spin, math.pi/4, 3, 0x2F0F00)
        ring.point(-spin*2, 1,  0x00FF00)
        ring.point(spin, 2, 0xFF0000)

        
        ring.draw()

        spin = (spin+(math.pi)/30)%(2*math.pi)
        if grow:
            width += math.pi / 30
            if width > 2*math.pi:
                grow = False
                angle += math.pi
        else:
            width -= math.pi / 30
            if width < 0:
                grow = True



        time.sleep(1.0/200)


hour = 0
minute = 0
second = 0

sec_angle = (2*math.pi)/60
while True:
    ring.point(second, 1, 0x0005F0)
    ring.line(minute, 1, 3, 0xF00000)
    ring.line(hour, 1, 2, 0xF000F0)
    

    ring.draw()

    second -= sec_angle
    minute -= sec_angle
    hour -= sec_angle/(12)

    time.sleep(1.0/100)

