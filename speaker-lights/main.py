import time
import argparse
from configparser import ConfigParser
import json
import os

from screen import Screen
from analyzer import Analyzer
from dbclient import DbClient
from layer import Layer

# get config file name from args
parser = argparse.ArgumentParser()
parser.add_argument("-C","--config", help="redis db connection details")
args = parser.parse_args()
configPath = args.config

# get server credentials from config
configur = ConfigParser()
configur.read(configPath)
servermode = 'cloud' # Either 'cloud' or 'local'
hostname = configur.get(servermode,'host')
password = configur.get(servermode,'password')
port = configur.getint(servermode, 'port')

#initialization
screen = Screen()
analyzer = Analyzer()

def handleLayerUpdate(lid, field, val):
    for layer in layers:
        if layer.lid == lid:
            print("found layer")
            layer.handleUpdate(field, val)

def handleSceneUpdate(field, layer=-1, lid=-1):
    global layers
    print("scene update")
    if field == 'new' and layer != -1:
        layers.append(layer)
    elif field == 'delete' and lid != -1:
        for layer in layers:
            if layer.lid == lid:
                layers.remove(layer)
    # if field == 'reorder':
    #     layers.sort(key=lambda x: x.index()) # sort by index
    #     print(layers)
    
    
db = DbClient(screen, analyzer, handleLayerUpdate, handleSceneUpdate, host=hostname, port=port, password=password)

def setup():
    global layers
    sid = db.getActive()
    layers = db.getLayers(sid)
    sources = []
    for layer in layers:
        layer.setAnalyzer(analyzer)
        sources.append(layer.getSource())
    analyzer.setSources(sources)
    print("Init Sources", sources)

def main():
    # for layer in layers:
    #   layer.draw(screen.ctx)
    # star.draw()
    #rms, bark, silent = analyzer.get()
    #screen.update(rms, bark, silent)
    time.sleep(1.0/100)

def test():
    global layers
    count = 0
    needsDraw = False
    screenClear = False
    while not db.kill:
        needsDraw = False
        index=len(layers)-1
        i = 0
        while index >= 0:
            for i in range(len(layers)):
                if layers[i].index() == index:
                    layers[i].update()
                    layers[i].draw(screen.ctx)
                    needsDraw = needsDraw or layers[i].visible()
                    index -= 1
                    break

        if needsDraw:
            screenClear = False
            screen.update()
        elif not screenClear:
            screenClear = True
            screen.clear()
        time.sleep(1/100.0)


def shutdown():
    db.stop()
    screen.close()
    analyzer.close()
    os.system('sudo python /home/pi/speaker-lights/speaker-lights/shutdown.py')
    

if __name__ == "__main__":
    count = 0
    setup()
    test()
    # while not db.kill:
    #     main()

    shutdown()
