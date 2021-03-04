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
    
    def divide_all(a,b):
        for i in range(len(a)):
            if b[i] != 0:
                a[i] = a[i] / b[i]
        return a
    
    

    def __init__(self):
        self.strip     = dotstar.DotStar(board.SCK, board.MOSI, Screen.numpixels,
                  brightness=1.0, auto_write=False, pixel_order=Screen.order)

        self.img = np.array(Screen.im)
        self.surface = cairo.ImageSurface.create_for_data(self.img,cairo.FORMAT_RGB24, Screen.width, Screen.height)
        self.ctx = cairo.Context(self.surface)
        
        self.scaled_bark = np.zeros(15)
        self.bass = 0.0
        self.scale_maxes = np.zeros(27)
    
    def update_scaled_bark(self, bark):
        max_change = 0.02
        
        if len(bark) == 27:
            for i in range(len(bark)):
                if bark[i] > self.scale_maxes[i]:
                    self.scale_maxes[i] = bark[i]
                else:
                    self.scale_maxes[i] *= 0.99
            
            jump = 0
            for i in range(len(self.scaled_bark)):
                if i<3:
                    b_norm = bark[i] / self.scale_maxes[i]
                    b_smooth = (b_norm + self.scaled_bark[i])/2
                    
                    if b_smooth - self.scaled_bark[i] > max_change:
                        self.scaled_bark[i] += max_change
                    elif self.scaled_bark[i] - b_smooth > max_change:
                        self.scaled_bark[i] -= max_change
                    else:
                        self.scaled_bark[i] = b_smooth
                else:
                    b1_norm = bark[i+jump] / self.scale_maxes[i+jump]
                    b2_norm = bark[i+jump+1] / self.scale_maxes[i+jump+1]
                    
                    b_smooth = (b1_norm+b2_norm)/2
                    b_smooth = (self.scaled_bark[i] +b_smooth)/2
                    
                    jump += 1
                    if b_smooth - self.scaled_bark[i] > max_change:
                        self.scaled_bark[i] += max_change
                    elif self.scaled_bark[i] - b_smooth > max_change:
                        self.scaled_bark[i] -= max_change
                    else:
                        self.scaled_bark[i] = b_smooth
            
            bass = (bark[0]+bark[1]+bark[2])/3
                
                

    def draw(self, img):
        count = 0
        for y in range(Screen.height):
            for x in range(Screen.width):
                strip_index = int(Screen.strip_map[y][x])
                if strip_index >= 0:
                    self.strip[strip_index] = (int(img[y][x][2]),int(img[y][x][1]),int(img[y][x][0]))
        self.strip.show()
    
    

    def update(self, bark=[0]):
        # clear canvas
        self.ctx.move_to(0,0)
        self.ctx.rectangle(0, 0, Screen.width, Screen.height)
        self.ctx.set_source_rgba(0,0,0,0.8)
        self.ctx.fill()
        # do stuff
#        pat = cairo.LinearGradient(0.0, Screen.height, 0.0, 0.0)
#        pat.add_color_stop_rgba(0, rms, 0, 0, 1)  # First stop, 50% opacity
#        pat.add_color_stop_rgba(1, 0.0, 0.0, rms, 1)  # Last stop, 100% opacity
#        self.ctx.set_source(pat)
#        self.ctx.fill()
            
        self.update_scaled_bark(bark)
        x = 5
        max_width = 7
        for y in range(Screen.height):
            val = min(self.scaled_bark[y], 1)
            s = min(max(val,0.7), 1)
            b = val/2
            hue = float(y) / Screen.height
            color = Color(hue=hue, saturation=s, luminance=b)
            r,g,b = color.rgb
            center_width = 7*val
            side_width = 4*val
            margin = (7 - center_width)/2
            self.ctx.rectangle(x,Screen.height-y, center_width, 1)
            self.ctx.rectangle(5-side_width,y, side_width, 1)
            self.ctx.rectangle(12,y, side_width, 1)
            self.ctx.set_source_rgb(r,g,b)  # Solid color
            self.ctx.set_line_width(0.25)
            self.ctx.fill()
            
#        bass_height = self.bass * 11
#        color = Color(hue=bass_height, saturation=0.9, luminance=bass_height)
#        r,g,b = color.rgb
#        pat1 = cairo.LinearGradient(0.0, 11, 4, 11-bass_height)
#        pat1.add_color_stop_rgba(0, r, g, b, 1)  # First stop, 50% opacity
#        pat1.add_color_stop_rgba(1, 0.0, 0.0, 0.0, 1)  # Last stop, 100%
#
#        pat2 = cairo.LinearGradient(12, 11, 16, 11-bass_height)
#        pat1.add_color_stop_rgba(0, r, g, b, 1)  # First stop, 50% opacity
#        pat1.add_color_stop_rgba(1, 0.0, 0.0, 0.0, 1)  # Last stop, 100%
#
#        self.ctx.rectangle(0,11-bass_height, 5, 0.5)
#        self.ctx.set_source(pat1)
#        self.ctx.fill() # Solid color
#        self.ctx.rectangle(12,11-bass_height, 5, 0.5)
#        self.ctx.set_source(pat2)
#        self.ctx.fill()
        
        # write to screen
        self.draw(self.img)

    def close(self):
        print('done')
