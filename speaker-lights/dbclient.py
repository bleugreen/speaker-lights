import redis
import json

from palette import Palette
from layer import Layer

class DbClient:
    changed = False
    
    def __init__(self, screen, analyzer, host='', port=0, password=''):
        if len(host) > 0:
            self.screen = screen
            self.analyzer = analyzer
            self.kill = False
            
            self.messenger = redis.Redis(host=host, port=port, password=password)
            self.client = redis.Redis(host=host, port=port, password=password)
            self.sub = self.messenger.pubsub()
            self.sub.subscribe(**{'active': self.handleMessage})
            self.thread = self.sub.run_in_thread(sleep_time=0.01)
            self.palette = []

            sid = self.client.get("scene:active").decode('utf-8')
            layers = self.client.zrange("scene:"+sid+":layers", 0, -1)
            print(layers)
    
    def handleMessage(self, message):
        data = message['data'].decode('utf-8').split(':')
        self.changed = True
        if len(data) > 0:
            if data[0] == 'switch':
                print("Mode Switch")
                #updateMode(modeid=data[1])
            elif data[0] == 'update':
                if data[1] == 'palette':
                    print("Palette Update")
                    self.updatePalette(pid=data[2])
                elif data[1] == 'sound':
                    print("Sound Update")
                    #updateSound(palid=data[2])
                elif data[1] == 'pattern':
                    print("Pattern Update")
                    #updatePattern(palid=data[2])
            elif data[0] == 'kill':
                self.kill = True
    
    def updatePalette(self, pid):
        data = self.client.hgetall("palette:"+pid)
        colors = self.client.lrange("palette:"+pid+":colors", 0, -1)
        print("name: "+data[b'name'].decode('utf-8'))
        if len(colors) > 0:
            in_palette = []
            for color in colors:
                in_palette.append(color.decode('utf-8'))
            
            self.palette = in_palette
            self.screen.setPalette(self.palette)
            #print(in_palette)
    
    def getActive(self):
        return self.client.get("scene:active").decode('utf-8')

    def getLayers(self,sid):
        layers = []
        data = self.client.zrange("scene:"+sid+":layers", 0, -1)
        for lid in data:
            layer = self.getLayer(lid.decode('utf-8'))
            layers.append(layer)
        print("length: ", len(layers))
        print("type: ", type(layers[0]))
        return layers
    
    def getLayer(self, lid):
        data = self.client.hgetall("layer:"+lid)
        layer_params = {}
        for key in data:
            layer_params[key.decode('utf-8')] = data[key].decode('utf-8')
        p = self.getPalette(layer_params['pid'])
        return Layer(lid, layer=layer_params, palette=p)


    def getPalette(self, pid):
        data = self.client.hgetall("palette:"+pid)
        lerp = (data[b'lerp'].decode('utf-8') == "true")
        colors = self.client.lrange("palette:"+pid+":colors", 0, -1)
        in_palette = []
        for color in colors:
            in_palette.append(color.decode('utf-8'))
        return Palette(colors=in_palette, lerp=lerp)


    
    # If database has received a message, returns true and toggles changed
    def hasChanged(self):
        if self.changed:
            self.changed = False
            return True
        else:
            return False
    
    def propogate(self, screen, analyzer):
        self.screen = screen
        self.analyzer = analyzer

    def stop(self):
        self.thread.stop()

    # getPalette(pid)
    # returns Palette

    # getLayer(lid)
    # returns Layer


    

    




