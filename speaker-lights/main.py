from pynput.keyboard import Listener
import atexit
import time

from screen import Screen
from analyzer import Analyzer

screen = Screen()
analyzer = Analyzer()

power_switch = True

def OnExitApp():
    print("Shutting down")
    analyzer.close()
    screen.close()
    print('done')
atexit.register(OnExitApp)

def main():
    x = analyzer.get_rms_ratio()
    screen.update(x)

if __name__ == "__main__":
    count = 0
    while count < 1000:
        main()
        count += 1