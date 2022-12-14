from typing import List, Tuple
from sqlalchemy import desc
from sqlalchemy.types import DateTime
from . import db

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String)
    time_stored = db.Column(DateTime)

def get_n_latest_images(n)->List[str]:
    latest_dates = (
        db.session.query(Image.time_stored)
        .order_by(Image.time_stored.desc())
        .limit(n)
        .all())
    return [date.date_column for date in latest_dates]