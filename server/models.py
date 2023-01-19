from typing import List, Tuple
from sqlalchemy import desc
from sqlalchemy.types import DateTime
from . import db, IMAGE_FOLDER
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from pathlib import Path

ALLOWED_EXTENSIONS = {'jpg'}
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer(), primary_key=True)
    file_name = db.Column(db.String(50), nullable = False)
    time_stored = db.Column(db.DateTime(), 
                            unique=True,
                            nullable=False)

def get_n_latest_images(n)->List[str]:
    update_database()
    images = db.session.query(Image).order_by(Image.time_stored.desc()).limit(n)
    images = [(image.file_name, image.time_stored.strftime("%Y-%m-%d %H:%M:%S")) for image in images]
    return images 

def allowed_file(filename):    
    split_str = filename.rsplit('.', 1)
    if len(split_str) != 2:
        return False
    
    datetime_str = split_str[0]
    exstension = split_str[1]
    
    year_time = filename.rsplit('.', 1)[0].lower()

    correct_datetime_format = is_correct_datetime_format(year_time)

    correct_extension = exstension.lower() in ALLOWED_EXTENSIONS
    is_filename = '.' in filename

    return  correct_extension and is_filename and correct_datetime_format 

def is_correct_datetime_format(year_time):
    correct_datetime_format = False
    # using try-except to check for truth value
    try:
        correct_datetime_format = bool(datetime.strptime(year_time, DATETIME_FORMAT))
    except ValueError:
        correct_datetime_format = False
    return correct_datetime_format

def remove_file_ending(file_name):
    return Path(file_name).stem

def filename_to_datetime(file_name):
    datetime_str = remove_file_ending(file_name)
    return datetime.strptime(datetime_str, DATETIME_FORMAT)
    

def get_images():
    file_names = os.listdir('static/images')
    allowed_files = [file for file in file_names if allowed_file(file)]
    secure_files = [secure_filename(file) for file in allowed_files]
    return ['images/' + image for image in secure_files]

def update_database():
    
    print(db)
    image_files = get_images()
    print(image_files)
    for file in image_files:
        # Check if the file is already in the database
        image = db.session.query(Image.file_name).filter_by(file_name=file).first()
        if not image:
            # File is not in the database, so add it
            image = Image(file_name=file, time_stored=filename_to_datetime(file))
            db.session.add(image)
            db.session.commit()
    
    images_in_db = [image_in_db.file_name for image_in_db in db.session.query(Image).all()]
    print(images_in_db)
    for db_im in images_in_db:
        if db_im not in image_files:
           db.session.query(Image).filter(Image.file_name == db_im).delete()
           db.session.commit()
        
