import redis
import json


class DbClient:
    changed = False
    
    def __init__(self, host='', port=0, password=''):
        if len(host) > 0:
            self.client = redis.Redis(host=host, port=port, password=password)
            self.sub = self.client.pubsub()
            self.sub.subscribe(**{'active': self.handleMessage})
            self.thread = self.sub.run_in_thread(sleep_time=0.01)
    def handleMessage(self, message):
        data = message['data'].decode('utf-8').split(',')
        self.changed = True
        print(data)
#        if len(data) > 0:
#            if data[0] == 'switch':
#                #updateMode(modeid=data[1])
#            elif data[0] == 'update':
#                if data[1] == 'palette':
#                    #updatePalette(palid=data[2])
#                elif data[1] == 'sound':
#                    #updateSound(palid=data[2])
#                elif data[1] == 'pattern':
#                    #updatePattern(palid=data[2])
    def hasChanged(self):
        if self.changed:
            self.changed = False
            return True
        else:
            return False



    

    




