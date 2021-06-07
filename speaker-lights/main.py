import time
import argparse
from configparser import ConfigParser
import json
import os

from screen import Screen
from analyzer import Analyzer
from dbclient import DbClient
import layer
from scene import Scene

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
scene = Scene()
db = DbClient(screen, analyzer, scene.handleUpdate, host=hostname, port=port, password=password)

def setup():
    sid = db.getActive()
    scene.setup(sid, db, analyzer, screen)

def main():
    # for layer in layers:
    #   layer.draw(screen.ctx)
    # star.draw()
    #rms, bark, silent = analyzer.get()
    #screen.update(rms, bark, silent)
    time.sleep(1.0/100)

def test():
    layers = scene.layers
    count = 0
    needsDraw = False
    screenClear = False
    while not db.kill:
        scene.draw()
        #time.sleep(1/100.0)


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
