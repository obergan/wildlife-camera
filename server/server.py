
from pathlib import Path
from werkzeug.utils import secure_filename
import os
from models import *
from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from heart import *
from apscheduler.schedulers.background import BackgroundScheduler

IMAGE_FOLDER = os.path.join(f'static', 'images')
HEART = Heart()

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'image_database')
app.config['UPLOAD_FOLDER'] = 'static/images'
app.secret_key = "key"
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def my_scheduled_task():
    HEART.update_status()
    pass
scheduler = BackgroundScheduler()
scheduler.add_job(my_scheduled_task, 'interval', seconds=30)

db.init_app(app)
with app.app_context():
    db.create_all()
    add_user("admin", "pass")

    

HOME_TAB = "home_page"
ABOUT_TAB = "about"
ADMIN_TAB = "admin"

TABS = {HOME_TAB : ("Home Page"), ABOUT_TAB : ("About"), ADMIN_TAB : ("Admin") }

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
    n = 20
    images = get_n_latest_images(n)
    active_tab = HOME_TAB
    HEART.update_status()
    if HEART.flat_line:
        status_str = "Inactive"
    else:
        status_str = "Active"

    time_since_changed_status = HEART.initial_timestamp
    formatted_datetime = time_since_changed_status.strftime("%Y-%m-%d %H:%M:%S")
    return render_general_page(active_tab=active_tab, 
                               images=images, 
                               camera_inactive=HEART.flat_line,
                               status_str = status_str, 
                               time_stamp=formatted_datetime,
                               num_img = str(len(images)))

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

@app.route('/heartbeat', methods=['POST'])
def hearbeat():
    hb = request.form['heartbeat']
    if hb == "beat":
        HEART.beat()
        return "Heartbeat recorded"
    else:
        return "Heartbeat failed"

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Replace this with your authentication logic (e.g., database lookup)
        user = get_user(request.form['username'], request.form['password'])
        if user:
            login_user(user)
            return redirect(url_for('admin'))

    return render_template("login.html")

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


if __name__ == "__main__":
    scheduler.start()
    app.run(host='0.0.0.0', debug=True)


    
