import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

red = 16
green = 18
blue = 22
sequence = [red, green, blue]

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
sleep = 1/10.

def setStatus(num):
    if num == 1:
        GPIO.output(sequence, (1, 0, 0))
    elif num == 2:
        GPIO.output(sequence, (0, 1, 0))
    elif num == 3:
        GPIO.output(sequence, (0, 0, 1))
    elif num == 0:
        GPIO.output(sequence, (0, 0, 0))


while True:
    setStatus(1)
    time.sleep(sleep)
    setStatus(2)
    time.sleep(sleep)
    setStatus(3)
    time.sleep(sleep)
    setStatus(0)
    time.sleep(sleep*3)
    # GPIO.output(sequence, (0, 0, 1)) 
    # time.sleep(sleep)

GPIO.cleanup(sequence)
