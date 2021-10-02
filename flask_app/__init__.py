from flask_ngrok import run_with_ngrok
from flask import Flask
import os

secret = os.urandom(24).hex()

app = Flask(__name__)
app.config['SECRET_KEY'] = secret
app.config['PLANTS_FOLDER'] = 'flask_app/static/plants'
app.config['LEAVES_FOLDER'] = 'flask_app/static/leaves'
app.config['SPOTS_FOLDER'] = 'flask_app/static/spots'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

from flask_app import routes

