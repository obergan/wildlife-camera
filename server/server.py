import flask
from pathlib import Path
from werkzeug.utils import secure_filename
import os
from server import models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from . import *

app = create_app()

DIR_LIST = ["1", "2", "3", "4"]

HOME_TAB = "home_page"
ABOUT_TAB = "about"
print(app.url_map)

TABS = {HOME_TAB : ("Home Page"), ABOUT_TAB : ("About")}

def render_general_page(active_tab, **kwargs) -> str:
    if active_tab in TABS:
        title = TABS[active_tab]
        page_to_render = f"{active_tab}.html"
    else:
        title = "Archive from year: " + active_tab
        page_to_render = f"year.html"
    
    years = [str(year) for year in models.get_years()]
    years.reverse()
    print(years)

    return flask.render_template(page_to_render, 
                                active_tab = active_tab, 
                                tabs = TABS.items(), 
                                title = title,
                                years = years, 
                                **kwargs)


@app.route("/")
def home_page():
    images = models.get_n_latest_images(5)
    active_tab = HOME_TAB
    return render_general_page(active_tab=active_tab, images=images)

@app.route("/about")
def about():
    image="images/portrait/me.jpg"
    active_tab = ABOUT_TAB
    return render_general_page(active_tab, portrait = image)

@app.route("/year/<int:year>")
def year_page(year):
    images = models.get_images_from_year(year)
    print("============")
    print(images)
    active_tab = str(year)
    return render_general_page(active_tab, images = images)

@app.get("/<path:path>")
def get_static(path):
    return flask.send_from_directory("static", path)
    
