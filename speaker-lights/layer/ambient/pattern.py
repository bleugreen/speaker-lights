import cairo

from palette import Palette
from screen import Screen

class Ambient:
    def drawLinearGradient(ctx, params, palette):
        panels = params.get('pos', 'center')

        if 'left' in panels and 'right' in panels and 'center' in panels:
            Ambient.drawLinearGradientHelper(ctx, params, palette, 0, 17, 17, 15)
        elif 'left' in panels and 'center' in panels:
            Ambient.drawLinearGradientHelper(ctx, params, palette, 0, 17, 12, 15)
        elif 'right' in panels and 'center' in panels:
            Ambient.drawLinearGradientHelper(ctx, params, palette, 5, 22, 12, 15)
        elif 'left' in panels and 'right' in panels:
            Ambient.drawLinearGradientHelper(ctx, params, palette, 0, 17, 5, 12)
            Ambient.drawLinearGradientHelper(ctx, params, palette, 12, 29, 5, 12, flip=True)
        elif 'left' in panels:
            Ambient.drawLinearGradientHelper(ctx, params, palette, 0, 17, 5, 12)
        elif 'right' in panels:
            Ambient.drawLinearGradientHelper(ctx, params, palette, 12, 29, 5, 12)
        elif 'center' in panels:
            Ambient.drawLinearGradientHelper(ctx, params, palette, 5, 22, 7, 15)
        

    def drawLinearGradientHelper(ctx, params, palette, l, r, w, h, flip=False):
        opacity = float(params.get('opacity', 100.0))/100.0
        direction = params.get('direction', 'down')
        width = w
        height = h
        l_start = l
        r_start = r 
        
        if flip:
            x2_L, y1_L, x1_L, y2_L = Ambient.getShape(direction, l_start, 0, width, height)
            x2_R, y1_R, x1_R, y2_R = Ambient.getShape(direction, r_start, 0, width, height)
        else:
            x1_L, y1_L, x2_L, y2_L = Ambient.getShape(direction, l_start, 0, width, height)
            x1_R, y1_R, x2_R, y2_R = Ambient.getShape(direction, r_start, 0, width, height)

        pat1 = cairo.LinearGradient(x1_L, y1_L, x2_L, y2_L)

        speakers = params.get('layout', 'left,right')
        if 'left' in speakers and 'right' in speakers:
            if params.get('tile', 'repeat') == 'mirror':
                pat2 = cairo.LinearGradient(x2_R, y1_R, x1_R, y2_R)
            else:
                pat2 = cairo.LinearGradient(x1_R, y1_R, x2_R, y2_R)
        else:
            pat2 = cairo.LinearGradient(x1_R, y1_R, x2_R, y2_R)
        Ambient.fillGradient(pat1, opacity, palette)
        Ambient.fillGradient(pat2, opacity, palette)
        
        if 'left' in speakers:
            ctx.set_source(pat1)
            ctx.rectangle(l_start, 0, width, height)
            ctx.fill()
        if 'right' in speakers:
            ctx.set_source(pat2)
            ctx.rectangle(r_start,0,width,height)
            ctx.fill()


    # adds color stops to gradient based on interpolated palette colors
    def fillGradient(pat, opacity, palette, steps=10):
        for i in range(steps):
            t = float(i)/(steps-1)
            r,g,b = palette.getColor(t)

            # if grayscale, match opacity to brightness
            if r==g and g==b:
                pat.add_color_stop_rgba(t, r, g, b, r)
            else:
                pat.add_color_stop_rgba(t, r, g, b, opacity)


    # returns start and end coordinates based on gradient dimensions and direction
    def getShape(direction, x, y, w, h):
        if direction == 'down':
            x_start, y_start = x, y
            x_end, y_end = x, h+y
        elif direction == 'up':
            x_start, y_start = x, h+y
            x_end, y_end = x, y
        elif direction == 'left':
            x_start, y_start = x+w, y
            x_end, y_end = x, y
        elif direction == 'right':
            x_start, y_start = x, y
            x_end, y_end = x+w, y
        elif direction == 'upright':
            x_start, y_start = x, y+h
            x_end, y_end = x+w, y
        elif direction == 'upleft':
            x_start, y_start = x+w, y+h
            x_end, y_end = x, y
        elif direction == 'downright':
            x_start, y_start = x, y
            x_end, y_end = x+w, y+h
        elif direction == 'downleft':
            x_start, y_start = x+w, y
            x_end, y_end = x, y+h
        return x_start,y_start,x_end,y_end
