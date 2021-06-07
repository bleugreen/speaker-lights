import cairo

from palette import Palette
from screen import Screen
from . import pattern as pt
from layer import Layer

# template class and utility methods for drawing and managing layers
class Ambient(Layer):
    def __init__(self, lid, layer={}, palette=0):
        super().__init__(lid, layer, palette)

    # gets newest data from analyzer
    def update(self):
        source = self.params.get('source', 'none')
        # self.data = self.analyzer.get(source)
        #print(self.data)
    
    
    # draws layer to screen
    def draw(self, ctx):
        visible = self.params.get('visible', 'false')
        pattern = self.params.get('pattern', 'lingradient')
        if visible == 'true':
            if pattern == 'lingradient':
                pt.Ambient.drawLinearGradient(ctx, self.params, self.palette)