
from pathlib import Path
from werkzeug.utils import secure_filename
import os
from models import *
from flask import Flask, request, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy

IMAGE_FOLDER = os.path.join(f'static', 'images')
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'image_database.
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'

db.init_app(app)
with app.app_context():
    db.create_all()


DIR_LIST = ["1", "2", "3", "4"]

HOME_TAB = "home_page"
ABOUT_TAB = "about"

TABS = {HOME_TAB : ("Home Page"), ABOUT_TAB : ("About")}

def render_general_page(active_tab, **kwargs) -> str:
    if active_tab in TABS:
        title = TABS[active_tab]
        page_to_render = f"{active_tab}.html"
    else:
        title = "Archive from year: " + active_tab
        page_to_render = f"year.html"

    years = [str(year) for year in get_years()]
    years.reverse()
    print(years)

    return render_template(page_to_render,
                                active_tab = active_tab,
                                tabs = TABS.items(),
                                title = title,
                                years = years,
                                **kwargs)


@app.route("/")
def home_page():
    images = get_n_latest_images(10)
    active_tab = HOME_TAB
    return render_general_page(active_tab=active_tab, images=images)

@app.route("/about")
def about():
    image="images/portrait/me.jpg"
    active_tab = ABOUT_TAB
    return render_general_page(active_tab, portrait = image)

@app.route("/year/<int:year>")
def year_page(year):
    update_database()
    images = get_images_from_year(year)

    active_tab = str(year)
    return render_general_page(active_tab, images = images)

@app.get("/<path:path>")
def get_static(path):
    return send_from_directory("static", path)

@app.route('/upload', methods=['POST'])
def upload():
    # Retrieve the JPG file and the text string from the request
    client_pw = request.form['password']
    system_pw = os.environ.get('FLASK_PASS')

    if (client_pw == system_pw):
        file = request.files['image']
        if file:
            filename = file.filename
            pt = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(pt)
            return "File uploaded!"
        else:
            return "No file found"

    return "Invalid password, breach detected"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


    
