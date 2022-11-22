import flask
from pathlib import Path
from werkzeug.utils import secure_filename
import os


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

def get_images():
    file_names = os.listdir('static/images')
    allowed_files = [file for file in file_names if allowed_file(file)]
    secure_files = [secure_filename(file) for file in allowed_files]
    return ['images/' + image for image in secure_files]

app = flask.Flask(__name__)

imageFolder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = imageFolder

ALLOWED_EXTENSIONS = {'jpg'}

@app.route("/")
def render_home_page():
    image_list = os.listdir('static/images')
    image_list = get_images()

    return flask.render_template(f"album.html", images=image_list)

@app.route("/about")
def render_about():
    image="images/img.jpg"
    return flask.render_template(f"about.html", portrait=image)

@app.get("/<path:path>")
def get_static(path):
    return flask.send_from_directory("static", path)
    
