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

def polar2index(r=1, theta=math.pi/2):
    while theta > math.pi*2:
        theta -= math.pi*2
    while theta < 0:
        theta += math.pi*2
    
    size   = 0
    offset = 0
    top    = 0
    
    if r==1:
        size   = 20.0
        offset = 100
        top = 6
    elif r==2:
        size   = 40.0
        offset = 60
        top = 33
    elif r==3:
        size   = 60.0
        top = 17.5
    else:
        return -1

    return int(offset+((size/(2*math.pi))*theta + top)%size)

class RingPoint:
    def __init__(self, angle, radius, color):
        self.radius = radius
        self.angle  = angle
        self.color  = color
    
    def draw(self, strip):
        index = polar2index(self.radius, self.angle)
        strip[index] = self.color

class RingArc:
    def __init__(self, angle, width, radius, color):
        self.radius = radius
        self.angle = angle
        self.width = width
        self.angle_start  = angle - width/2.0
        self.angle_end  = angle + width/2.0
        self.color  = color
    
    def draw(self, strip):
        start = polar2index(self.radius, self.angle_start)
        end = polar2index(self.radius, self.angle_end)
        if self.radius == 3:
            offset = 0
            size = 60
        elif self.radius == 2:
            offset = 60
            size = 40
        elif self.radius == 1:
            offset = 100
            size =  20
        else:
            return

        start = polar2index(self.radius, self.angle_start)
        ledWidth = int((self.width/(2*math.pi))*size)

        index = (start-offset)
        for i in range(ledWidth):
            strip[index+offset] = self.color
            index = (index+1)%size

            
class RingLine:
    def __init__(self, angle, r1, r2, color):
        self.angle = angle
        self.radius_start  = min(r1, r2)
        self.radius_end  = max(r1, r2)
        self.color  = color

    def draw(self, strip):
        radius = self.radius_start

        while radius <= self.radius_end:
            index = polar2index(radius, self.angle)
            strip[index] = self.color
            radius += 1

class RingFan:
    def __init__(self, angle, width, color):
        self.angle = angle
        self.color  = color
        self.width  = width
    
    def draw(self, strip):
        width3 = self.width/2.0

        arc1 = RingArc(self.angle, self.width, 3,self.color)
        arc2 = RingArc(self.angle, self.width, 2, self.color)
        arc3 = RingArc(self.angle, self.width, 1, self.color)

        arc1.draw(strip)
        arc2.draw(strip)
        arc3.draw(strip)


class Ring:
    top1 = 6
    top2 = 33
    top3 = 17.5

    size = 120
    size1 = 20.0
    size2 = 40.0
    size3 = 60.0

    def __init__(self, strip):
        self.draw_list = []
        self.strip = strip
    
    def point(self, angle, radius, color):
        pt  = RingPoint(angle, radius, color)
        self.draw_list.append(pt)

    def arc(self, angle, width, radius, color):
        arc = RingArc(angle, width, radius, color)
        self.draw_list.append(arc)
    
    def line(self, angle, r1, r2, color):
        arc = RingLine(angle, r1, r2, color)
        self.draw_list.append(arc)
    
    def fan(self, angle, width, color):
        fan = RingFan(angle, width, color)
        self.draw_list.append(fan)

    def polar2index(self, r=1, theta=math.pi/2):
        size   = 0
        offset = 0
        top    = 0
        
        if r==1:
            size   = 20.0
            offset = 100
            top = 6

        elif r==2:
            size   = 40.0
            offset = 60
            top = 33

        elif r==3:
            size   = 60.0
            top = 17.5

        else:
            return -1

        return offset+int((size/(2*math.pi))*theta + top)%size
    
    def draw(self):
        for i in range(120):
            self.strip[i] = 0
        for obj in self.draw_list:
            obj.draw(self.strip)
            self.draw_list.remove(obj)
        self.strip.show()

