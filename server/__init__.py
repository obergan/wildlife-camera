# # import flask and sqlaclhemy
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# import os
# IMAGE_FOLDER = os.path.join(f'static', 'images')
# basedir = os.path.abspath(os.path.dirname(__file__))
# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__, instance_relative_config=False)
#     #app.config.from_object("config.Config")

#     app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'image_database.db')
   
#     # app configuration
#     db.init_app(app)
#     with app.app_context():
#         from . import server
#         from . import models
#         db.create_all()

#     return app


