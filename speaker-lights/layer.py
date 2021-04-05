from palette import Palette

# template class and utility methods for drawing and managing layers
class Layer:
    def __init__(self, lid, context, analyzer, 
                    opacity=0.0, pid=-1, source='none',pos='full'):
        self.lid = lid
        self.opacity = opacity
        self.pid = pid
        self.palette = Palette()
        self.source = source
        self.pos = pos
        self.ctx = context
        self.analyzer = analyzer
    
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
