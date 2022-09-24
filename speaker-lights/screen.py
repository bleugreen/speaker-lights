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

from palette import Palette

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# 226 pixels per speaker, covering a 17x15 area
class Screen:
    numpixels = 226 #+circle           #
    order     = dotstar.BGR  #

    stripmap_left_path = os.path.join(THIS_FOLDER, 'stripmap_left.csv')
    stripmap_right_path = os.path.join(THIS_FOLDER, 'stripmap_right.csv')

    stripmap_right = list(csv.reader(open(stripmap_right_path)))
    stripmap_left = list(csv.reader(open(stripmap_left_path)))

    height = len(stripmap_left)
    width = len(stripmap_left[0])*2

    def __init__(self, layout='RL'):
        self.strip_left    = dotstar.DotStar(board.SCK, board.MOSI, Screen.numpixels,
                  brightness=0.8, auto_write=False, pixel_order=Screen.order)
        self.strip_right     = dotstar.DotStar(board.SCK_1, board.MOSI_1, Screen.numpixels,
                  brightness=0.8, auto_write=False, pixel_order=Screen.order)

        self.img = np.ones((Screen.height,Screen.width,4), dtype='uint8')
        self.surface = cairo.ImageSurface.create_for_data(self.img,cairo.FORMAT_RGB24, Screen.width, Screen.height)
        self.ctx = cairo.Context(self.surface)

        self.right_offset = 1
        self.left_offset = 1

        self.hasChanged = False


    # Translates Cairo image to LED output
    def draw(self, img, dest='left'):
        for y in range(Screen.height):
            for x in range(int(Screen.width/2)):
                left_index = int(Screen.stripmap_left[y][x])
                if left_index >= 0:
                    left_index += self.left_offset
                    self.strip_left[left_index] = (int(img[y][x][2]),int(img[y][x][1]),int(img[y][x][0]))
                right_index = int(Screen.stripmap_right[y][x])
                if right_index >= 0:
                    right_index += self.right_offset
                    right_x = int(x+(Screen.width/2))
                    self.strip_right[right_index] = (int(img[y][right_x][2]),int(img[y][right_x][1]),int(img[y][right_x][0]))

        self.strip_left.show()
        self.strip_right.show()

    def getCtx(self):
        self.hasChanged = True
        return self.ctx


    def update(self):
        if self.hasChanged:
            # write to screen
            self.draw(self.img)

            # clear drawing surface
            self.ctx.set_source_rgba(0,0,0,0.8)
            self.ctx.paint()
            self.hasChanged = False

        # self.drawStar()

    def clear(self):
        self.ctx.set_source_rgba(0,0,0,1)
        self.ctx.paint()
        self.draw(self.img)

    def close(self):
        print('done')
