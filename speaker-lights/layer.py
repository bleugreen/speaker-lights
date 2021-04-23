from palette import Palette
import cairo

from screen import Screen

# template class and utility methods for drawing and managing layers
class Layer:
    def __init__(self, lid, layer={}, palette=0):
        #print(layer)
        self.lid = lid
        self.params = layer
        print(self.params)
        #print("Got: "+self.type)
        #print(self.opacity)
        if palette == 0:
            self.palette = Palette()
        else:
            self.palette = palette

        self.data = 0

    def handleUpdate(self, field, val):
        print('name: '+self.params['name'])
        print('field: '+field)
        
        if field == 'palette':
            self.palette = val
            print(len(self.palette.palette))
        else:
            print('val: '+val)
            self.params[field] = val


    def getSource(self):
        return self.params['source']

    def setAnalyzer(self, analyzer):
        self.analyzer = analyzer
    
    def update(self):
        self.data = self.analyzer.get(self.params['source'])
        #print(self.data)
    
    def draw(self, ctx):
        if self.params['visible'] == 'true':
            self.testPattern(ctx)
    
    def index(self):
        return int(self.params['index'])

    def visible(self):
        return (self.params['visible'] == 'true') or int(self.params['opacity']) == 0

    # returns x_min, y_min, width, height for position
    def getBounds(self):
        if self.pos == 'center':
            return 5, 0, 7, 15
        elif self.pos == 'full':
            return 0, 0, 17, 15
        elif self.pos == 'left':
            return 0, 0, 5, 12
        elif self.pos == 'right':
            return 12, 0, 5, 12

    def testPattern(self, ctx):
        opacity = float(self.params['opacity'])/100.0
        direction = self.params.get('direction', "down")

        if direction == 'down':
            x_start = 0
            x_end = 0
            y_start = 0
            y_end = Screen.height
        elif direction == 'up':
            x_start = 0
            x_end = 0
            y_start = Screen.height
            y_end = 0
        elif direction == 'left':
            x_start = Screen.width
            x_end = 0
            y_start = 0
            y_end = 0
        elif direction == 'right':
            x_start = 0
            x_end = Screen.width
            y_start = 0
            y_end = 0
        pat1 = cairo.LinearGradient(x_start, y_start, x_end, y_end)
        if self.palette.lerp:
            steps = 10
            for i in range(steps):
                t = float(i)/(steps-1)
                r,g,b = self.palette.getColor(t)
                pat1.add_color_stop_rgba(t, r, g, b, opacity)
        else:
            r1,g1,b1 = self.palette.getColor(0)
            pat1.add_color_stop_rgba(0, r1, g1, b1, opacity)
            r2,g2,b2 = self.palette.getColor(1)
            pat1.add_color_stop_rgba(1, r2, g2, b2, opacity)

        ctx.set_source(pat1)
        layout = self.params['layout']
        panels = self.params['pos']

        # draw rectable for each active panel/speaker
        if 'left' in layout:
            if 'left' in panels:
                ctx.rectangle(0, 0, 5, 12)
            if 'center' in panels:
                ctx.rectangle(5, 0, 7, 15)
            if 'right' in panels:
                ctx.rectangle(12, 0, 5, 12)
        if 'right' in layout:
            if 'left' in panels:
                ctx.rectangle(17, 0, 5, 12)
            if 'center' in panels:
                ctx.rectangle(22, 0, 7, 15)
            if 'right' in panels:
                ctx.rectangle(29, 0, 5, 12)
        ctx.fill()
