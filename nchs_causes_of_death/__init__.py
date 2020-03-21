# __init__.py tells python this is a package and initializes/ties together 
# what our app needs to run
from flask import Flask

# Init app
app = Flask(__name__)

from nchs_causes_of_death import routes