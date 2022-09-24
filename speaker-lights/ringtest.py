#!/usr/bin/python3

# Simple strand test for Adafruit Dot Star RGB LED strip.
# This is a basic diagnostic tool, NOT a graphics demo...helps confirm
# correct wiring and tests each pixel's ability to display red, green
# and blue and to forward data down the line.  By limiting the number
# and color of LEDs, it's reasonably safe to power a couple meters off
# USB.  DON'T try that with other code!

from multiprocessing import cpu_count
import time
import board
import adafruit_dotstar as dotstar
from colour import Color
import math
from rings import Ring
from palette import Palette


def lerp(a, b, t):
    return (1-t)*a + t*b


numpixels = 350           # Number of LEDs in strip
order     = dotstar.BGR  # Might need GRB instead for older DotStar LEDs
strip     = dotstar.DotStar(board.SCK, board.MOSI, numpixels,
              brightness=0.15, auto_write=False, pixel_order=order)
ring = Ring(strip)

palette = Palette(['red', 'green', 'blue', 'red'])

b = 0.25
# Fill inner ring
frames = 20.0
angle = math.pi
radius = 1
innercolor = 0
color_range=20/120.
color_start = 0
for i in range(int(frames)):
    t = ((i)/frames)*(color_range)-(color_range)
    if t < 0:
        t += 1
    color_raw = palette.getColor(t)
    color = (int(color_raw[0]*255), int(color_raw[1]*255), int(color_raw[2]*255), b)
    innercolor = color
    width = ((i+1)/frames)*2*math.pi
    ring.arc(angle, width, radius, color)
    ring.draw()
    time.sleep(1/100.0)

# Fill middle ring
frames = 40.0
angle = math.pi
radius = 2
midcolor=0
color_range=40/120.
color_start = 20/120.
for i in range(int(frames)):
    t = color_start + (((i)/frames)*(color_range))-color_range
    if t < 0:
        t += 1
    color_raw = palette.getColor(t)
    color = (int(color_raw[0]*255), int(color_raw[1]*255), int(color_raw[2]*255), b)
    midcolor = color
    width = ((i+1)/frames)*2*math.pi
    ring.arc(0, 2*math.pi, 1, innercolor)
    ring.arc(angle, width, radius, color)
    ring.draw()
    time.sleep(1/100.0)

frames = 60.0
angle = math.pi
radius = 3
outercolor =0
color_range=60/120.
color_start = 60/120.
for i in range(int(frames)):
    t = color_start+ (((i)/frames)*(color_range))-color_range
    color_raw = palette.getColor(t)
    color = (int(color_raw[0]*255), int(color_raw[1]*255), int(color_raw[2]*255), b)
    outercolor = color
    width = ((i+1)/frames)*2*math.pi
    ring.arc(0, 2*math.pi, 1, innercolor)
    ring.arc(0, 2*math.pi, 2, midcolor)
    ring.arc(angle, width, radius, color)
    ring.draw()
    time.sleep(1/150.0)

# Fade to white
frames = 20.0
for i in range(int(frames)):
    inner0 = int(lerp(innercolor[0], 255, (i+1)/frames))
    inner1 = int(lerp(innercolor[1], 255, (i+1)/frames))
    inner2 = int(lerp(innercolor[2], 255, (i+1)/frames))
    ring.arc(0, 2*math.pi, 1, (inner0,inner1,inner2, b))
    mid0 = int(lerp(midcolor[0], 255, (i+1)/frames))
    mid1 = int(lerp(midcolor[1], 255, (i+1)/frames))
    mid2 = int(lerp(midcolor[2], 255, (i+1)/frames))
    ring.arc(0, 2*math.pi, 2, (mid0,mid1,mid2, b))
    out0 = int(lerp(outercolor[0], 255, (i+1)/frames))
    out1 = int(lerp(outercolor[1], 255, (i+1)/frames))
    out2 = int(lerp(outercolor[2], 255, (i+1)/frames))
    ring.arc(0, 2*math.pi, 3, (out0,out1,out2, b))
    ring.draw()
    time.sleep(1/50.)

# Fade to black
for i in range(50):
    color = int(lerp(255, 0, (i+1)/50.0))
    ring.arc(0, 2*math.pi, 1, (color,color,color, b))
    ring.arc(0, 2*math.pi, 2, (color,color,color, b))
    ring.arc(0, 2*math.pi, 3, (color,color,color, b))
    ring.draw()
    time.sleep(1/100.)

# Final clear
ring.draw()