import time
import argparse
from configparser import ConfigParser
import json
import os


from screen import Screen
from analyzer import Analyzer
from dbclient import DbClient

# get config file name from args
parser = argparse.ArgumentParser()
parser.add_argument("-c","--config", help="redis db connection details")
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
db = DbClient(screen, analyzer, host=hostname, port=port, password=password)

def main():
    rms, bark, silent = analyzer.get()
    screen.update(rms, bark, silent)
    time.sleep(1.0/100)

def shutdown():
    db.stop()
    screen.close()
    analyzer.close()
    os.system('sudo shutdown -h now')

if __name__ == "__main__":
    count = 0

    while not db.kill:
        main()
        
    shutdown()
