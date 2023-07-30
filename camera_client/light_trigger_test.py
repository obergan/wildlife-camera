import RPi.GPIO as GPIO
import time
import requests
import subprocess
import os
from datetime import datetime, timedelta

GPIO.cleanup() 
GPIO.setwarnings(False)


MOSFET_PIN = 13


GPIO.setmode(GPIO.BOARD)
GPIO.setup(MOSFET_PIN, GPIO.OUT)

def control_led(state):
    GPIO.output(MOSFET_PIN, state)


for i in range(1):
    control_led(GPIO.HIGH)
    time.sleep(50)
    command = ["raspistill", "-w", '640', '-h', '480', "-o","/home/camera/camera_client/test.jpg"]
    subprocess.run(command)
    time.sleep(2)
    control_led(GPIO.LOW)
    time.sleep(5)
    print(i)
    
    
GPIO.cleanup()
