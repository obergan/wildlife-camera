
from pathlib import Path
import os


HOME_TAB = "Home Page"
ABOUT_TAB = "About"

TABS = {HOME_TAB : ("home_page"), ABOUT_TAB : ("about")}
for (key, val) in TABS.items():
    print(key, val)

print(TABS.items()) 