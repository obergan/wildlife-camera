
import time
import requests
import subprocess
import os
from datetime import datetime, timedelta
import logging


HEARTBEAT_URL = "http://127.0.0.1:5000/heartbeat"



payload={'heartbeat': 'beat'}
headers = {}
response = requests.request("POST", HEARTBEAT_URL, headers=headers, data=payload)
print(response.text)


print("Unable to post image")

