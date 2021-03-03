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
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

class Screen:
    numpixels = 225           #
    order     = dotstar.BGR  #

    stripmap_path = os.path.join(THIS_FOLDER, 'stripmapping.csv')
    strip_map = list(csv.reader(open(stripmap_path)))
    height = len(strip_map)
    width = len(strip_map[0])

    im = Image.open('example.png')
    im.putalpha(256)

    def __init__(self):
        self.strip     = dotstar.DotStar(board.SCK, board.MOSI, Screen.numpixels,
                  brightness=1.0, auto_write=False, pixel_order=Screen.order)

        self.img = np.array(Screen.im)
        self.surface = cairo.ImageSurface.create_for_data(self.img,cairo.FORMAT_RGB24, Screen.width, Screen.height)
        self.ctx = cairo.Context(self.surface)

    def draw(self, img):
        count = 0
        for y in range(Screen.height):
            for x in range(Screen.width):
                strip_index = int(Screen.strip_map[y][x])
                if strip_index >= 0:
                    self.strip[strip_index] = (int(img[y][x][2]),int(img[y][x][1]),int(img[y][x][0]))
        self.strip.show()

    def update(self, rms=0):
        # clear canvas
        self.ctx.rectangle(0, 0, Screen.width, Screen.height)
        print(rms)
        # do stuff
        pat = cairo.LinearGradient(0.0, Screen.height, 0.0, 0.0)
        pat.add_color_stop_rgba(0, rms, 0, 0, 1)  # First stop, 50% opacity
        pat.add_color_stop_rgba(1, 0.0, 0.0, 1-rms, 1)  # Last stop, 100% opacity
        self.ctx.set_source(pat)
        self.ctx.fill()

        # write to screen
        self.draw(self.img)

    def close(self):
        print('done')