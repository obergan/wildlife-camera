# import flask and sqlaclhemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    # app configuration
    db.init_app(app)
    with app.app_context():
        from . import server
        from . import models
        db.create_all()

    return app


# import models
from server import models
