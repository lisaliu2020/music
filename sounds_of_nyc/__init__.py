from flask import Flask

sounds_of_nyc = Flask(__name__)

from sounds_of_nyc import routes
