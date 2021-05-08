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

class Screen:
    numpixels = 474           #
    order     = dotstar.BGR  #

    star_len = 0 #22
    buffer_len = 1
    speaker_len = 225

    starmap_path = os.path.join(THIS_FOLDER, 'starmap.csv')
    stripmap_left_path = os.path.join(THIS_FOLDER, 'stripmap_left.csv')
    stripmap_right_path = os.path.join(THIS_FOLDER, 'stripmap_right.csv')
    
    starmap = list(csv.reader(open(starmap_path)))
    stripmap_right = list(csv.reader(open(stripmap_right_path)))
    stripmap_left = list(csv.reader(open(stripmap_left_path)))
    
    height = len(stripmap_right)
    width = len(stripmap_right[0])*2

    def __init__(self, layout='RL'):
        self.strip     = dotstar.DotStar(board.SCK, board.MOSI, Screen.numpixels,
                  brightness=1.0, auto_write=False, pixel_order=Screen.order)

        self.img = np.ones((Screen.height,Screen.width,4), dtype='uint8')
        self.star_img = np.full((len(Screen.starmap), len(Screen.starmap[0])), Color('black'))
        self.surface = cairo.ImageSurface.create_for_data(self.img,cairo.FORMAT_RGB24, Screen.width, Screen.height)
        self.ctx = cairo.Context(self.surface)

        offset1 = Screen.star_len + Screen.buffer_len
        offset2 = offset1 + Screen.buffer_len+Screen.speaker_len

        if layout=='LR':
            self.left_offset = offset1
            self.right_offset = offset2
        else:
            self.left_offset = offset2
            self.right_offset = offset1
            
    
    # Translates Cairo images to LED output        
    def draw(self, img, dest='left'):
        # x:(0,16) = L
        # x:(17,33) = R
        #if RL:
        # r_offset = 22
        # l_offset = 247
        for y in range(Screen.height):
            #left
            for x in range(int(Screen.width/2)):
                strip_index = int(Screen.stripmap_left[y][x])
                if strip_index >= 0:
                    self.strip[strip_index+self.left_offset] = (int(img[y][x][2]),int(img[y][x][1]),int(img[y][x][0]))
            #right
            for x in range(int(Screen.width/2)):
                strip_index = int(Screen.stripmap_right[y][x])
                if strip_index >= 0:
                    self.strip[strip_index+self.right_offset] = (int(img[y][x+int(Screen.width/2)][2]),int(img[y][x+int(Screen.width/2)][1]),int(img[y][x+int(Screen.width/2)][0]))
                    # if y==13 and x == 8:
                        # print('right:')
                        # print(int(img[y][x+int(Screen.width/2)][2]),int(img[y][x+int(Screen.width/2)][1]),int(img[y][x+int(Screen.width/2)][0]))
        self.strip.show()

    
    def getdata(self):
        print(self.scaled_bark[0])

    def setLayout(self, layout):
        if layout == 'RL':
            self.right_offset = 22-22
            self.left_offset = 247-22
        else:
            self.right_offset = 247-22
            self.left_offset = 22-22
        

    def update(self):
        # write to screen
        self.draw(self.img)

        # clear drawing surface
        self.ctx.set_source_rgba(0,0,0,1)
        self.ctx.paint()

        # self.drawStar()
    
    def clear(self):
        self.ctx.set_source_rgba(0,0,0,1)
        self.ctx.paint()
        self.draw(self.img)

    def close(self):
        print('done')
