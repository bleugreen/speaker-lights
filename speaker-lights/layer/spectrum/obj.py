import cairo

from palette import Palette
from screen import Screen

from layer import Layer

# template class and utility methods for drawing and managing layers
class Spectrum(Layer):
    def __init__(self, lid, layer={}, palette=0):
        super().__init__(lid, layer, palette)
        self.ave = 5.0
        self.data = []
        self.data_max = []
        self.startx = 5.
        self.starty = 0.
        self.width = 7.
        self.height = 15.
        self.silent = True

    # gets newest data from analyzer
    def update(self):
        source =  'bark' # self.params.get('source', 'none')
        in_data = self.analyzer.getSpec(source)
        self.silent = self.analyzer.get('silent')
        if len(in_data) > 0:
            if len(self.data) != len(in_data):
                self.data = in_data
                self.data_max = in_data
            else:
                for i in range(len(in_data)):
                    if in_data[i] > self.data_max[i]:
                        self.data_max[i] = in_data[i]
                    
                    norm = float(in_data[i]) / self.data_max[i]
                    # if i == 0:
                    #     print(norm, len(self.data))
                    old = self.data[i]
                    self.data[i] = (old - (old / self.ave)) + (norm / self.ave)
        #print(self.data)
    
    # draws layer to screen
    def draw(self, ctx):
        visible = self.params.get('visible', 'false')
        pattern = self.params.get('pattern', 'lingradient')
        if visible == 'true' and not self.silent:
            self.drawGraph(ctx)
            #print('drawing')
    
    def drawGraph(self, ctx):
        mirrorx = self.params.get('mirrorx', 'true') == 'false'
        mirrory = self.params.get('mirrory', 'true') == 'true'
        

        if mirrorx and mirrory:
            self.drawGraphMirrorXY(ctx)
        elif mirrorx:
            self.drawGraphMirrorX(ctx)
        elif mirrory:
            self.drawGraphMirrorY(ctx)
        else:
            self.drawGraphNoMirror(ctx)

    def drawGraphMirrorXY(self,ctx):
        tile = self.params.get('tile', 'repeat')
        barHeight = (self.height / len(self.data))/2
        x = self.startx
        y = 0
        opacity = float(self.params.get('opacity', 100)) / 100.0

        ctx.move_to(0,0)
        for i in range(len(self.data)):
            t = float(i) / (len(self.data)-1)
            val = self.data[i]
            barWidth = self.width * val
            margin = self.width - barWidth
            r,g,b = self.palette.getColor(t)
            ctx.set_source_rgb(r,g,b)
            
            ctx.rectangle(x, y, barWidth/2, barHeight)
            ctx.rectangle(x, self.height-y, barWidth/2, barHeight)

            ctx.rectangle(x+margin, y, barWidth/2, barHeight)
            ctx.rectangle(x+margin, self.height-y, barWidth/2, barHeight)
            
            ctx.rectangle(x+17, y, barWidth, barHeight)
            ctx.rectangle(x+17, self.height-y, barWidth, barHeight)
            
            ctx.fill()
            y += barHeight

    def drawGraphMirrorX(self,ctx):
        tile = self.params.get('tile', 'repeat')
        barHeight = self.height / len(self.data)
        x = self.startx
        y = 0
        opacity = float(self.params.get('opacity', 100)) / 100.0

        ctx.move_to(0,0)
        for i in range(len(self.data)):
            t = float(i) / (len(self.data)-1)
            val = self.data[len(self.data)-1-i]
            barWidth = self.width * val
            margin = self.width - barWidth
            r,g,b = self.palette.getColor(t)
            ctx.set_source_rgb(r,g,b)
            
            ctx.rectangle(x, y, barWidth/2, barHeight)
            ctx.rectangle(x+margin, y, barWidth/2, barHeight)
            
            ctx.rectangle(x+17, y, barWidth, barHeight)
            
            ctx.fill()
            y += barHeight

    def drawGraphMirrorY(self,ctx):
        tile = self.params.get('tile', 'repeat')
        barHeight = (self.height / len(self.data))/2
        x = self.startx
        y = 0
        opacity = float(self.params.get('opacity', 100)) / 100.0

        ctx.move_to(0,0)
        for i in range(len(self.data)):
            t = float(i) / (len(self.data)-1)
            val = self.data[len(self.data)-1-i]
            barWidth = self.width * val
            margin = self.width - barWidth
            r,g,b = self.palette.getColor(t)
            ctx.set_source_rgb(r,g,b)
            
            ctx.rectangle(x, y, barWidth, barHeight)
            ctx.rectangle(x, self.height-y, barWidth, barHeight)
            
            ctx.rectangle(x+17, y, barWidth, barHeight)
            ctx.rectangle(x+17, self.height-y, barWidth, barHeight)
            
            ctx.fill()
            y += barHeight

    def drawGraphNoMirror(self,ctx):
        tile = self.params.get('tile', 'repeat')
        barHeight = self.height / len(self.data)
        x = self.startx
        y = 0
        opacity = float(self.params.get('opacity', 100)) / 100.0

        ctx.move_to(0,0)
        for i in range(len(self.data)):
            t = float(i) / (len(self.data)-1)
            val = self.data[len(self.data)-1-i]
            barWidth = self.width * val
            r,g,b = self.palette.getColor(t)
            ctx.set_source_rgb(r,g,b)
            
            ctx.rectangle(x, y, barWidth, barHeight)
            ctx.rectangle(x+17, y, barWidth, barHeight)
            
            ctx.fill()
            y += barHeight

