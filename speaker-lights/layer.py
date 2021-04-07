from palette import Palette

# template class and utility methods for drawing and managing layers
class Layer:
    def __init__(self, lid, layer={}, palette=0):
        #print(layer)
        self.type = layer['type'] if 'type' in layer else 'ambient'
        self.opacity = int(layer['opacity']) if 'opacity' in layer else 0
        self.pos = layer['location'] if 'location' in layer else 'none'
        self.source = layer['source'] if 'source' in layer else 'none'
        self.pattern = layer['pattern'] if 'pattern' in layer else 'none'
        #print("Got: "+self.type)
        #print(self.opacity)
        if palette == 0:
            self.palette = Palette()
        else:
            self.palette = palette


    def getSource(self):
        return self.source
    
    def update(self, data):
        print('update received - '+self.lid)
        print(data)
    
    def draw(self, ctx):
        print(self.lid+": draw")
    
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
