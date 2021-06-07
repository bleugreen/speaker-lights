import layer

# template class and utility methods for drawing and managing layers
class Scene:

    def setup(self, sid, db, analyzer, screen):
        self.sid = sid
        self.db = db
        self.analyzer = analyzer
        self.screen = screen
        
        self.layers = sorted(db.getLayers(sid), key=lambda x: x.index(), reverse=True)
        self.sources = []
        for layer in self.layers:
            layer.setAnalyzer(analyzer)
            self.sources.append(layer.getSource())
        analyzer.setSources(self.sources)
        print(self.sources)

        self.needsDraw = False
        self.screenClear = False

    
    def handleUpdate(self, target='', id='', action='', field='', val=''):
        if target == 'scene' and id == self.sid:
            if action == 'reorder':
                self.layers = sorted(self.layers, key=lambda x: x.index(), reverse=True)
            if action == 'new':
                layer = self.db.getLayer(field)
                layer.setAnalyzer(self.analyzer)
                self.layers.append(layer)
                self.layers = sorted(self.layers, key=lambda x: x.index(), reverse=True)
                for layer in self.layers:
                    print('layer:', layer.params.get('name'), ' index=', layer.index())
            if action == 'delete':
                for layer in self.layers:
                    if layer.lid == field:
                        print('deleting layer: '+field)
                        
                        self.layers.remove(layer)
                        self.layers = sorted(self.layers, key=lambda x: x.index(), reverse=True)
                        for layer in self.layers:
                            print('layer:', layer.params.get('name'), ' index=', layer.index())
            if action == 'change':
                self.layers = self.db.getLayers(self.sid)
                self.sources = []
                for layer in self.layers:
                    layer.setAnalyzer(self.analyzer)
                    self.sources.append(layer.getSource())
                self.analyzer.setSources(self.sources)

        if target == 'layer':
            for layer in self.layers:
                if layer.lid == id:
                    if action == 'update':
                        if field == 'pid':
                            palette = self.db.getPalette(val)
                            layer.handleUpdate('palette', palette)
                        else:
                            layer.handleUpdate(field, val)
    
    def draw(self):
        if not self.needsDraw:
            self.screen.clear()
        
        self.needsDraw = False
        i = 0
        for layer in self.layers:
            layer.update()
            layer.draw(self.screen.ctx)
            self.needsDraw = self.needsDraw or layer.visible()

        if self.needsDraw:
            self.screen.update()

            


        

        
    
    