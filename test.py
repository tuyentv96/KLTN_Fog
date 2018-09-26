import RPi.GPIO as GPIO
import time

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

while True:
    GPIO.output(11, 1)
    GPIO.output(13, 1)
    time.sleep(1)
    GPIO.output(11, 0)
    GPIO.output(13, 0)
    time.sleep(1)
