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
    numpixels = 247           #
    order     = dotstar.BGR  #

    stripmap_path = os.path.join(THIS_FOLDER, 'stripmapping.csv')
    strip_map = list(csv.reader(open(stripmap_path)))
    
    star_map = np.array([[8,10,15,17,19,21,4,6],
                         [7,9,14,16,18,20,3,5],
                         [13,2,-1,-1,-1,-1,-1,-1],
                         [12,1,-1,-1,-1,-1,-1,-1],
                         [0,11,-1,-1,-1,-1,-1,-1,]])
    palette_star = np.array([[0.5,0.25,0,0.25,0.5,0.25,0,0.25],
                         [0.75,0.5,0.25,0.5,0.75,0.5,0.25,0.5],
                         [0.5,0.5,-1,-1,-1,-1,-1,-1],
                         [0.75,0.75,-1,-1,-1,-1,-1,-1],
                         [1.0,1.0,-1,-1,-1,-1,-1,-1,]])
    
    height = len(strip_map)
    width = len(strip_map[0])

    im = Image.open('example.png')
    im.putalpha(256)
    
    spectrumMode = 'split'
    
    def divide_all(a,b):
        for i in range(len(a)):
            if b[i] != 0:
                a[i] = a[i] / b[i]
        return a
    
    

    def __init__(self):
        self.strip     = dotstar.DotStar(board.SCK, board.MOSI, Screen.numpixels,
                  brightness=0.9, auto_write=False, pixel_order=Screen.order)

        self.img = np.array(Screen.im)
        self.surface = cairo.ImageSurface.create_for_data(self.img,cairo.FORMAT_RGB24, Screen.width, Screen.height)
        self.ctx = cairo.Context(self.surface)
        
        self.scaled_bark = np.zeros(27)
        self.bass = 0.0
        self.scale_maxes = np.zeros(27)
        self.bouncet = 0
        self.v = 0.005
        self.rms = 0
        self.palette = Palette()
    
    def update_scaled_bark(self, bark):
        max_change = 0.05
        min_change = 0.01
        
        if len(bark) == 27:
            for i in range(len(bark)):
                if bark[i] > self.scale_maxes[i]:
                    self.scale_maxes[i] = bark[i]
                else:
                    self.scale_maxes[i] *= 0.99
            for i in range(len(bark)):
                b_norm = bark[i] / self.scale_maxes[i]
                b_smooth = (b_norm + self.scaled_bark[i])/2
                    
                if b_smooth - self.scaled_bark[i] > max_change:
                    self.scaled_bark[i] += max_change
                elif self.scaled_bark[i] - b_smooth > max_change:
                    self.scaled_bark[i] -= max_change
                elif abs(self.scaled_bark[i] - b_smooth) > min_change:
                    self.scaled_bark[i] = b_smooth
                
            
           
    def gradientFade(self, bouncet):
        self.ctx.rectangle(0, 0, Screen.width, Screen.height)
        pat = cairo.LinearGradient(0, 0, Screen.width, Screen.height)
        
        r1,g1,b1 = self.palette.getColor(bouncet)
        r2,g2,b2 = self.palette.getColor(bouncet*0.6)
        pat.add_color_stop_rgba(0, r1, g1, b1, 1)  # First stop, 50% opacity
        pat.add_color_stop_rgba(1, r2, g2, b2, 1)  # Last stop, 100% opacity
        self.ctx.set_source(pat)
        self.ctx.fill()
                
    #input - 8x8 array of colors
    def drawStar(self, input=[]):
        if len(input) > 0:
            for i in range(len(Screen.star_map)):
                for j in range(len(Screen.star_map[0])):
                    strip_index = Screen.star_map[i][j]
                    color = input[i][j]
                    
                    self.strip[strip_index] = color
            self.strip.show()
        else:
            for i in range(len(Screen.star_map)):
                for j in range(len(Screen.star_map[0])):
                    strip_index = Screen.star_map[i][j]
                    
                    if strip_index >= 0:
                        color = self.palette.getColor(Screen.palette_star[i][j])
                        b = self.rms*self.rms
                        maxb = 75
                        if i==0:
                            if b>0.5:
                                b=0
                            else:
                                b = min((b*2), 1)*maxb
                        if i==1:
                            b = max(0, b-0.5)*2*maxb
                        if i >1:
                            b = max(0, b-0.8)*2*maxb
                        self.strip[strip_index] = (int(color[0]*b),int(color[1]*b),int(color[2]*b))
            self.strip.show()
            
        
        
    
    def draw(self, img, dest='left'):
        count = 0
        if dest == 'left':
            for y in range(Screen.height):
                for x in range(Screen.width):
                    strip_index = int(Screen.strip_map[y][x])+22
                    if strip_index >= 0:
                        self.strip[strip_index] = (int(img[y][x][2]),int(img[y][x][1]),int(img[y][x][0]))
            self.strip.show()
        elif dest == 'right':
            for y in range(Screen.height):
                for x in range(Screen.width):
                    strip_index = int(Screen.strip_map[y][x])+247
                    if strip_index >= 0:
                        self.strip[strip_index] = (int(img[y][x][2]),int(img[y][x][1]),int(img[y][x][0]))
            self.strip.show()
    
    def getdata(self):
        print(self.scaled_bark[0])
        
    def setPalette(self, in_palette):
        self.palette.setPalette(in_palette)
        
    def drawTestPattern(self):
        for i in range(Screen.height):
            self.ctx.rectangle(0, i, Screen.width, 1)
            
            r,g,b = self.palette.getColor(float(i) / Screen.height)
            self.ctx.set_source_rgb(r,g,b)  # Solid color
            self.ctx.set_line_width(0.25)
            self.ctx.fill()
        

    def update(self, rms=0, bark=[0], silent=False):
        # clear canvas
        self.rms = rms
        
        self.ctx.move_to(0,0)
        self.ctx.rectangle(0, 0, Screen.width, Screen.height)
        self.ctx.set_source_rgba(0,0,0,0.5)
        self.ctx.fill()
        # do stuff
#        pat = cairo.LinearGradient(0.0, Screen.height, 0.0, 0.0)
#        pat.add_color_stop_rgba(0, rms, 0, 0, 1)  # First stop, 50% opacity
#        pat.add_color_stop_rgba(1, 0.0, 0.0, rms, 1)  # Last stop, 100% opacity
#        self.ctx.set_source(pat)
#        self.ctx.fill()
        
        #self.drawTestPattern()
        
        if silent:
            self.gradientFade(self.bouncet)
            self.bouncet += self.v
            if self.bouncet > 1 or self.bouncet < 0:
                self.v *= -1
                self.bouncet += self.v
            
        self.update_scaled_bark(bark)
        center_start = 5
        center_end = 12
        max_width = 7
        barHeight = (float(Screen.height) / len(bark))/2
        
        
        for i in range(len(self.scaled_bark)):
            y = (float(i) / len(self.scaled_bark))*(Screen.height-1)
            y = y/2
            val = self.scaled_bark[i]
            center_width = max_width*val
            margin = (7 - center_width)/2
            r,g,b = self.palette.getColor(float(i) / len(self.scaled_bark))
            if Screen.spectrumMode == 'split':
                self.ctx.rectangle(center_start,Screen.height-(y), center_width/2, barHeight)
                self.ctx.rectangle(center_end-center_width/2,Screen.height-(y), center_width/2, barHeight)
                self.ctx.rectangle(center_start,y, center_width/2, barHeight)
                self.ctx.rectangle(center_end-center_width/2,y, center_width/2, barHeight)
            self.ctx.set_source_rgb(r,g,b)  # Solid color
            self.ctx.set_line_width(0.25)
            self.ctx.fill()
            bass = rms
            if bass > 0.8:
                bass_height = (bass-0.8)*5*12
                by = 12-bass_height
                r,g,b = self.palette.getColor(bass_height/20)
                self.ctx.rectangle(0,by,5,bass_height)
                self.ctx.rectangle(12,by,5,bass_height)
                self.ctx.set_source_rgb(r,g,b)  # Solid color
                self.ctx.set_line_width(0.25)
                self.ctx.fill()
                
                
#        for y in range(Screen.height):
#            cval = (self.scaled_bark[y])
#            bass = 1-rms
#
#            #val = min(val, 1)
#
#            r,g,b = self.palette.getColor(float(y) / Screen.height)
#            center_width = 15*cval
#            side_width = 5*bass
#
#            if Screen.spectrumMode == 'split':
#                self.ctx.rectangle(center_start,Screen.height-(y+1), center_width/2, 1)
#                self.ctx.rectangle(center_end-center_width/2,Screen.height-(y+1), center_width/2, 1)
#            else:
#                self.ctx.rectangle(center_start+margin,Screen.height-(y+1), center_width, 1)
            #self.ctx.rectangle(5-side_width,y, side_width, 1)
            #self.ctx.rectangle(12,y, side_width, 1)
            
            
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
        self.drawStar()

    def close(self):
        print('done')
