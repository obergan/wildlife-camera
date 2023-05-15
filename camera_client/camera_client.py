import RPi.GPIO as GPIO
import time
import requests
import subprocess
import os
from datetime import datetime

GPIO.cleanup() 
GPIO.setwarnings(False)


PIR = 11
LED = 3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, 0)         #LED output pin

def read_motion_sensor():
    return GPIO.input(PIR) == 1

def grad_and_upload_image():
    
    filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.jpg')
    filepath = os.path.join('images', filename)
    grab_image(filepath, filename)
    
    url = "http://wildlifecamera.ddns.net/upload"
    try:
        payload={'password': 'mango'}
        files=[('image',(filename,open(filepath,'rb'),'images/jpeg'))]
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        
        print(response.text)
    except:
        print("Unable to post image")
    
def grab_image(filepath, filename):
    command = ["raspistill", "-w", '640', '-h', '480', "-o", filepath]
    subprocess.run(command)
    print("Image aquired!")

# Initialize variables
previous_state = False
current_state = False
run_loop = True
count = 0

# Create a directory named "images" if it does not already exist
if not os.path.exists('images'):
    os.makedirs('images')

try:
    while run_loop:
        current_state = read_motion_sensor()
        
        if current_state == True:
            print("Motion detected")
            GPIO.output(3, 1)  #Turn ON LED
            time.sleep(0.1)
            grad_and_upload_image()
            count = count + 1
            if count >=2:
                run_loop = False        
            
        if current_state == False:
            print("No motion")
            GPIO.output(3, 0)
            time.sleep(0.1)             
        
        previous_state = read_motion_sensor()

except KeyboardInterrupt:
    GPIO.cleanup()    
