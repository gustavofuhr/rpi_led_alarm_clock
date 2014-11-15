import RPi.GPIO as GPIO
from time import sleep

channel = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)
GPIO.output(channel, GPIO.HIGH)

sleep(10)

GPIO.cleanup()
