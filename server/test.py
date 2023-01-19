
from sqlalchemy.types import DateTime


import os
from datetime import datetime
from pathlib import Path

ALLOWED_EXTENSIONS = {'jpg'}
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

def allowed_file(filename):    
    split_str = filename.rsplit('.', 1)
    if len(split_str) != 2:
        return False
    
    datetime_str = split_str[0]
    exstension = split_str[1]
    
    year_time = filename.rsplit('.', 1)[0].lower()

    correct_datetime_format = False
    # using try-except to check for truth value
    try:
        correct_datetime_format = bool(datetime.strptime(year_time, DATETIME_FORMAT))
    except ValueError:
        correct_datetime_format = False

    correct_extension = exstension.lower() in ALLOWED_EXTENSIONS
    is_filename = '.' in filename

    return  correct_extension and is_filename and correct_datetime_format

def remove_file_ending(file_name):
    return Path(file_name).stem

def filename_to_datetime(file_name):
    datetime_str = remove_file_ending(file_name)
    return datetime.strptime(datetime_str, DATETIME_FORMAT)

test = [("bajs", "kiss"), ("lars", "bajja")]

for key, value in test:
    print(key, value)