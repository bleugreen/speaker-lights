import redis
import json
import os
import time
import argparse
from configparser import ConfigParser

killSignal = False

def handleMessage(message):
        global thread, client
        data = message['data'].decode('utf-8').split(':')
        print(data)
        if len(data) > 0:
            if data[0] == 'start':
               os.system('sudo python /home/pi/speaker-lights/speaker-lights/main.py --config /home/pi/speaker-lights/speaker-lights/config.ini')
            elif data[0] == 'reboot':
                client.set("connected", "false")
                client.publish("pi2site", "connected:false")
                client.set("running", "false")
                client.publish("pi2site", "running:false")
                thread.stop()
                os.system('sudo python /home/pi/speaker-lights/speaker-lights/shutdown.py')
                os.system('sudo reboot')
            elif data[0] == 'shutdown':
                client.set("connected", "false")
                client.set("running", "false")
                client.publish("pi2site", "running:false")
                client.publish("pi2site", "connected:false")
                
                thread.stop()
                os.system('sudo python /home/pi/speaker-lights/speaker-lights/shutdown.py')
                os.system('sudo shutdown -h now')
            
def main():
    global thread, client
    #os.system('sudo python /home/pi/speaker-lights/speaker-lights/startup.py')

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
    while True:
        try:
            client = redis.Redis(host=hostname, port=port, password=password)
            messenger = redis.Redis(host=hostname, port=port, password=password)
            sub = messenger.pubsub()
            sub.subscribe(**{'util': handleMessage})
            thread = sub.run_in_thread(sleep_time=0.1)
            client.set("connected", "true")
            client.publish("pi2site", "connected:true")
            client.set("running", "false")
            client.publish("pi2site", "running:false")
            os.system('sudo python /home/pi/speaker-lights/speaker-lights/startup.py')
            return 
        except:
            pass
    

main()




