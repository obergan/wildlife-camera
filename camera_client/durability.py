import RPi.GPIO as GPIO
import time
import requests
import subprocess
import os
from datetime import datetime, timedelta
import logging

GPIO.cleanup() 
GPIO.setwarnings(False)


PIR = 11
MOSFET_PIN = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(MOSFET_PIN, GPIO.OUT)

UPLOAD_URL = "http://wildlifecamera.ddns.net/upload"
UPLOAD_PASSWORD = 'mango' # change to system variable
IMAGE_DIR = 'images'
IMAGE_INTERVAL_SECONDS = 60


def read_motion_sensor():
    return GPIO.input(PIR) == 1

def grad_and_upload_image():
    filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.jpg')
    filepath = os.path.join(IMAGE_DIR, filename)
    grab_image(filepath, filename)
    upload_image(filepath, filename)
    
def grab_image(filepath, filename):
    command = ["raspistill", "-w", '640', '-h', '480', "-o", filepath]
    subprocess.run(command)
    print("Image aquired!")
    
def upload_image(filepath, filename):
    try:
        payload={'password': UPLOAD_PASSWORD}
        files=[('image',(filename,open(filepath,'rb'),'images/jpeg'))]
        headers = {}
        response = requests.request("POST", UPLOAD_URL, headers=headers, data=payload, files=files)
        
        print(response.text)
    except:
        print("Unable to post image")


def control_led(state):
    GPIO.output(MOSFET_PIN, state)

# Initialize variables
previous_state = False
current_state = False
run_loop = True
count = 0
last_image_time = datetime.now()
start_time = datetime.now()

# Create a directory named "images" if it does not already exist
if not os.path.exists('images'):
    os.makedirs('images')

# Set up logging
logging.basicConfig(filename='camera.log', level=logging.INFO, format='%(asctime)s - %(message)s')
msg = f"================= NEW SESSION ================="
logging.info(msg)

try:
    while run_loop:
        motion_detected = read_motion_sensor()
        time_elapsed = datetime.now() - last_image_time
                
        if (time_elapsed >= timedelta(seconds = IMAGE_INTERVAL_SECONDS)): #and motion_detected:
            
            control_led(GPIO.HIGH)
            print("LED ON")
            time.sleep(5)
            grad_and_upload_image()
            print("Image aquired after: ", time_elapsed, " seconds")
            print("LED OFF")
            control_led(GPIO.LOW)
            last_image_time = datetime.now()
            duration = last_image_time - start_time
            minutes = duration.total_seconds()//60
            count = count + 1
            log_message = f"Program have been live for {minutes} minutes. Images taken = {count}"
            logging.info(log_message)
            time.sleep(0.1)             

except KeyboardInterrupt:
    GPIO.cleanup()    
