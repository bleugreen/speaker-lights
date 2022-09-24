from stringsim import String
from screen import Screen
import random
import time
import numpy as np
screen = Screen()
string1 = String(nodes=15, center=25, color='green')
string2 = String(nodes=15, center=25, color='red')
string3 = String(nodes=15, center=25, color='blue')
def main():
    t = time.time()
    t2 = time.time()
    t3 = time.time()
    while True:
        string1.draw(screen.getCtx())
        string2.draw(screen.getCtx())
        string3.draw(screen.getCtx())
        screen.update()
        if time.time() - t2 > 3:
            t2 = time.time()
            data = np.zeros(15)
            data[5] = random.randrange(40,60) if random.randrange(0,2) == 1 else -random.randrange(40,60)
            string2.update(data)
            string2.update(data)
        if time.time() - t3 > 2:
            t3 = time.time()
            data = np.zeros(15)
            data[7] = random.randrange(20,50) if random.randrange(0,2) == 1 else -random.randrange(20,50)
            string3.update(data)
            string3.update(data)
        if time.time() - t > 5:
            t = time.time()
            data = np.zeros(15)
            data[9] = random.randrange(30,60) if random.randrange(0,2) == 1 else -random.randrange(30,60)
            string1.update(data)
            string1.update(data)

        else:
            string1.update(np.zeros(15))
            string2.update(np.zeros(15))
            string3.update(np.zeros(15))


main()