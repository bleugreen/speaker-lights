import redis
import json
import os
import time
import argparse
from configparser import ConfigParser

killSignal = False

def handleMessage(message):
        global killSignal
        data = message['data'].decode('utf-8').split(':')
        print(data)
        if len(data) > 0:
            if data[0] == 'start':
               os.system('sudo python main.py --config config.ini')
            elif data[0] == 'shutdown':
                killSignal = True
                #os.system('sudo python shutdown -h now')
            
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

client = redis.Redis(host=hostname, port=port, password=password)
sub = client.pubsub()
sub.subscribe(**{'util': handleMessage})
thread = sub.run_in_thread(sleep_time=0.1)

os.system('sudo python startup.py')

while not killSignal:
    time.sleep(1)
thread.stop()
os.system('sudo python startup.py')

