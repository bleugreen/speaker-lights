import redis
import json

from palette import Palette
import layer

class DbClient:
    changed = False
    
    def __init__(self, screen, analyzer, sceneUpdate, host='', port=0, password='', update=''):
        if len(host) > 0:
            # Assign object references
            self.screen = screen
            self.analyzer = analyzer

            # Assign update callbacks
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
            else:
                # print(data)
                self.sceneUpdate(target=data[0], id=data[1], action=data[2], field=data[3], val=data[4])
            
    
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
        type = layer_params.get('type', 'ambient')
        if type == 'ambient':
            return layer.Ambient(lid, layer=layer_params, palette=p)
        elif type == 'spectrum':
            print('creating spectrum layer', layer_params)
            return layer.Spectrum(lid, layer=layer_params, palette=p)


    def getPalette(self, pid):
        # print(pid)
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


    

    




