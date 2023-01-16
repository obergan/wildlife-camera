from typing import List, Tuple
from sqlalchemy import desc
from sqlalchemy.types import DateTime
from . import db, IMAGE_FOLDER
from werkzeug.utils import secure_filename
import os
from datetime import datetime

ALLOWED_EXTENSIONS = {'jpg'}

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String)
    time_stored = db.Column(DateTime)

def get_n_latest_images(n)->List[str]:
    update_database()
    latest_dates = (
        db.session.query(Image.time_stored)
        .order_by(Image.time_stored.desc())
        .limit(n)
        .all())
    return [date.date_column for date in latest_dates]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

def get_images():
    file_names = os.listdir('static/images')
    allowed_files = [file for file in file_names if allowed_file(file)]
    secure_files = [secure_filename(file) for file in allowed_files]
    return ['images/' + image for image in secure_files]

def update_database():
    image_files = get_images()
    for file in image_files:
        # Check if the file is already in the database
        image = db.session.query(Image).filter_by(time_stored=file).first()
        if not image:
            # File is not in the database, so add it
            image = Image(file_name=file, datetime=datetime.now())
            db.session.add(image)
            db.session.commit()

update_database()