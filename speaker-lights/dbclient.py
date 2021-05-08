import redis
import json

from palette import Palette
from layer import Layer

class DbClient:
    changed = False
    
    def __init__(self, screen, analyzer, layerUpdate, sceneUpdate, host='', port=0, password='', update=''):
        if len(host) > 0:
            # Assign object references
            self.screen = screen
            self.analyzer = analyzer

            # Assign update callbacks
            self.layerUpdate = layerUpdate
            self.sceneUpdate = sceneUpdate

            # Init killswitch
            self.kill = False
            
            # Init Redis client (sends messages / sets values)
            self.client = redis.Redis(host=host, port=port, password=password)

            # Init Redis messenger (receives messages)
            self.messenger = redis.Redis(host=host, port=port, password=password)
            self.sub = self.messenger.pubsub()
            self.sub.subscribe(**{'active': self.handleMessage})
            self.thread = self.sub.run_in_thread(sleep_time=0.01)
            
            self.client.set("running", "true")
            self.client.publish("pi2site", "running:true")


    
    def handleMessage(self, message):
        data = message['data'].decode('utf-8').split(':')
        self.changed = True
        if len(data) > 0:
            if data[0] == 'kill':
                self.kill = True
            if data[0] == 'scene':
                if data[1] == 'reorder':
                    self.sceneUpdate("reorder")
                elif data[1] == 'new':
                    layer = self.getLayer(data[2])
                    self.sceneUpdate('new', layer=layer)
                elif data[1] == 'delete':
                    self.sceneUpdate('delete', lid=data[2])
            elif data[0] == 'layer':
                lid = data[1]
                if data[2] == 'pid':
                    print("Palette Update")
                    palette = self.getPalette(data[3])
                    self.layerUpdate(lid,"palette", palette)
                else:
                    self.layerUpdate(lid,data[2], data[3])
            
    
    def getActive(self):
        return self.client.get("scene:active").decode('utf-8')

    def getLayers(self,sid):
        # decode layer list
        layers = []
        data = self.client.zrange("scene:"+sid+":layers", 0, -1)
        for lid in data:
            layer = self.getLayer(lid.decode('utf-8'))
            layers.append(layer)
        # print("length: ", len(layers))
        # print("type: ", type(layers[0]))

        # return list
        return layers
    
    def getLayer(self, lid):
        # decode layer hash
        data = self.client.hgetall("layer:"+lid)
        layer_params = {}
        for key in data:
            layer_params[key.decode('utf-8')] = data[key].decode('utf-8')
        
        # build palette from pid
        p = self.getPalette(layer_params['pid'])

        # return full layer
        return Layer(lid, layer=layer_params, palette=p)


    def getPalette(self, pid):
        print(pid)
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
        self.client.set("running", "false")
        self.client.publish("pi2site", "running:false")
        self.thread.stop()

    # getPalette(pid)
    # returns Palette

    # getLayer(lid)
    # returns Layer


    

    




