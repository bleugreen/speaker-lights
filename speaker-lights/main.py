from pynput.keyboard import Listener
import time
#test

from screen import Screen
from analyzer import Analyzer

screen = Screen()
analyzer = Analyzer()

def main():
    x = analyzer.get_rms_ratio()
    screen.update(x)

if __name__ == "__main__":
    count = 0
    while count < 10000:
        main()
        count += 1
    screen.close()
    analyzer.close()