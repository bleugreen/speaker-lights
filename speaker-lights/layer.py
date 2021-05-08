from palette import Palette
import cairo

from screen import Screen
from ambient import Ambient

# template class and utility methods for drawing and managing layers
class Layer:
    def __init__(self, lid, layer={}, palette=0):
        #print(layer)
        self.lid = lid
        self.params = layer
        print(self.params)
        if palette == 0:
            self.palette = Palette()
        else:
            self.palette = palette

        self.data = 0

    # callback used to react to db changes
    def handleUpdate(self, field, val):
        print('Layer Update:')
        print('name: '+self.params.get('name', 'no name'))
        print('field: '+field)
        
        if field == 'palette':
            self.palette = val
        elif field == 'source':
            oldSource = self.params['source']
            self.params['source'] = val
            self.analyzer.updateSources(oldSource, val)
        else:
            print('val: '+val)
            self.params[field] = val

    # returns data source of layer
    def getSource(self):
        return self.params.get('source', 'none')

    # set/reset ref to analyzer
    def setAnalyzer(self, analyzer):
        self.analyzer = analyzer
    
    # gets newest data from analyzer
    def update(self):
        source = self.params.get('source', 'none')
        self.data = self.analyzer.get(source)
        #print(self.data)
    
    # draws layer to screen
    def draw(self, ctx):
        visible = self.params.get('visible', 'false')
        pattern = self.params.get('pattern', 'lingradient')
        if visible == 'true':
            if pattern == 'lingradient':
                Ambient.drawLinearGradient(ctx, self.params, self.palette)
            if pattern == 'rain':
                self.rain = Ambient.drawRain(ctx, self.params, self.palette, self.rain)
    
    # returns z-index of layer
    def index(self):
        return int(self.params.get('index', 0))

    # returns true if layer needs to be drawn
    def visible(self):
        visible = self.params.get('visible', 'false')
        opacity = int(self.params.get('opacity', 0))
        return (visible == 'true') or (opacity == 0)


