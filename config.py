import os

class Config:
    """Configuration of Flask app"""

    #FLASK_ENV = 'development'
    #SECRET_KEY = os.environ["SECRET_KEY"]

    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    imageFolder = os.path.join(STATIC_FOLDER, 'images')
    UPLOAD_FOLDER = imageFolder


    SQLALCHEMY_DATABASE_URI = 'sqlite:///image_database.db' #os.environ["SQLALCHEMY_DATABASE_URI"]