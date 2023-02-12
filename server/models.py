from typing import List, Tuple, Dict
from sqlalchemy import desc, extract, distinct
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

# image info = (path, date-time string)
def get_image_info(images)->List[Tuple[str, str]]:     
    return [(image.file_name, image.time_stored.strftime("%Y-%m-%d %H:%M:%S")) for image in images]


def get_n_latest_images(n)->List[str]:
    update_database()
    images = db.session.query(Image).order_by(Image.time_stored.desc()).limit(n)
    return get_image_info(images) 

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
    
    image_files = get_images()
    for file in image_files:
        # Check if the file is already in the database
        image = db.session.query(Image.file_name).filter_by(file_name=file).first()
        if not image:
            # File is not in the database, so add it
            image = Image(file_name=file, time_stored=filename_to_datetime(file))
            db.session.add(image)
            db.session.commit()
    
    images_in_db = [image_in_db.file_name for image_in_db in db.session.query(Image).all()]

    for db_im in images_in_db:
        if db_im not in image_files:
            # if db entry does not exist in directory, delete it
           db.session.query(Image).filter(Image.file_name == db_im).delete()
           db.session.commit()

def get_years():
    years = db.session.query(extract('year', Image.time_stored)).distinct().all()
    return [year[0] for year in years]

def get_images_from_year(year)->Dict[str, Tuple[str, str]]:
    image_dict = {}
    # Ectract every image-filled month
    months = db.session.query(extract('month', Image.time_stored)).filter(extract('year', Image.time_stored) == year).distinct().all()
    months = [month[0] for month in months]

    # Example February : [(path1, date1), (path2, date2)]
    for month in months:
        images_in_month = db.session.query(Image).filter(extract('year', Image.time_stored) == year,
                                                         extract('month', Image.time_stored) == month).all()
        image_info = get_image_info(images_in_month)
        print(image_info)
        image_dict[month_from_number(month)] = image_info

    return image_dict

def month_from_number(month_number):
    month_names = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    if month_number >= 0 and month_number <= 12:
        return month_names[month_number-1]
    else:
        return "Invalid month number"




