import flask
from pathlib import Path
from werkzeug.utils import secure_filename
import os

DIR_LIST = ["1", "2", "3", "4"]

HOME_TAB = "home_page"
ABOUT_TAB = "about"

TABS = {HOME_TAB : ("Home Page"), ABOUT_TAB : ("About")}

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


def render_general_page(active_tab, **kwargs) -> str:
    title = TABS[active_tab]
    return flask.render_template(f"{active_tab}.html", active_tab = active_tab, tabs = TABS.items(), title = title, **kwargs)


@app.route("/")
def home_page():
    image_list = os.listdir('static/images')
    image_list = get_images()
    active_tab = HOME_TAB
    return render_general_page(active_tab=active_tab, images=image_list)

@app.route("/about")
def about():
    image="images/img.jpg"
    active_tab = ABOUT_TAB
    return render_general_page(active_tab, portrait = image)

@app.get("/<path:path>")
def get_static(path):
    return flask.send_from_directory("static", path)
    
