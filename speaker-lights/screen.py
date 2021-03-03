#!/usr/bin/python3

# Screen wrapper to allow drawing to LED strip as 2D cairo ImageSurface
from PIL import Image
import board
import csv
import random
import adafruit_dotstar as dotstar
from colour import Color
import math
import cairo
import numpy as np

class Screen:
    numpixels = 225           #
    order     = dotstar.BGR  #

    strip_map = list(csv.reader(open('/home/pi/PseudoEgo/stripmapping.csv')))
    height = len(strip_map)
    width = len(strip_map[0])

    im = Image.open('example.png')
    im.putalpha(256)

    def __init__(self):
        self.strip     = dotstar.DotStar(board.SCK, board.MOSI, numpixels,
                  brightness=1.0, auto_write=False, pixel_order=order)

        self.img = np.array(im)
        self.surface = cairo.ImageSurface.create_for_data(self.img,cairo.FORMAT_RGB24, width, height)
        self.ctx = cairo.Context(self.surface)

    def draw(self, img):
        count = 0
        for y in range(height):
            for x in range(width):
                strip_index = int(strip_map[y][x])
                if strip_index != 250:
                    self.strip[strip_index] = (int(img[y][x][2]),int(img[y][x][1]),int(img[y][x][0]))
        self.strip.show()

    def update(self, rms=0):
        # clear canvas
        self.ctx.rectangle(0, 0, width, height)
        print(rms)
        # do stuff
        pat = cairo.LinearGradient(0.0, 0.0, height, width)
        pat.add_color_stop_rgba(0, rms, 0, 0, 1)  # First stop, 50% opacity
        pat.add_color_stop_rgba(1, 0.0, 0.0, 1-rms, 1)  # Last stop, 100% opacity
        self.ctx.set_source(pat)
        self.ctx.fill()

        # write to screen
        self.draw(self.img)

    def close(self):
        print('done')