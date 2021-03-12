import time
import argparse
from configparser import ConfigParser
import json

from screen import Screen
from analyzer import Analyzer
from dbclient import DbClient

parser = argparse.ArgumentParser()
parser.add_argument("-c","--config", help="redis db connection details")
args = parser.parse_args()
configPath = args.config

configur = ConfigParser()
configur.read(configPath)
servermode = 'cloud' # Either 'cloud' or 'local'
hostname = configur.get(servermode,'host')
password = configur.get(servermode,'password')
port = configur.getint(servermode, 'port')




screen = Screen()
analyzer = Analyzer()
db = DbClient(host=hostname, port=port, password=password)

def main():
    bark = analyzer.get_bark()
    screen.update(bark)

if __name__ == "__main__":
    count = 0
    while count < 10000:
        time.sleep(0.1)
        if db.hasChanged():
            # db.propogate(screen, analyzer)
    thread.stop()
    screen.close()
    analyzer.close()
