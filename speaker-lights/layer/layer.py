import cairo

from palette import Palette
from screen import Screen

# template class and utility methods for drawing and managing layers
class Layer:
    def __init__(self, lid, layer={}, palette=0):
        #print(layer)
        self.lid = lid
        self.params = layer
        # print(self.params)
        if palette == 0:
            self.palette = Palette()
        else:
            self.palette = palette

    # callback used to react to db changes
    def handleUpdate(self, field, val):
        if field == 'palette':
            self.palette = val
            val = val.palette
        elif field == 'source':
            oldSource = self.params['source']
            self.params['source'] = val
            self.analyzer.updateSources(oldSource, val)
        else:
            self.params[field] = val
        print('Update: (',self.params.get('name', 'no name'),') ',field,' = ', val)

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
    
    # returns z-index of layer
    def index(self):
        return int(self.params.get('index', 100)) # end of list by default

    # returns true if layer needs to be drawn
    def visible(self):
        visible = self.params.get('visible', 'false')
        opacity = int(self.params.get('opacity', 0))
        return (visible == 'true') or (opacity == 0)


