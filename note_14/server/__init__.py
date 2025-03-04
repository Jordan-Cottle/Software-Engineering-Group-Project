""" Initialization file for the server package.

The flask application object is created here and is available for import at the package level.
"""
# pylint: disable=wrong-import-position

import os

from flask import Flask
from flask_login import LoginManager

from database import inject_session, close_session
from config import SECRET_KEY, UPLOAD_FOLDER, ALLOWED_EXTENSIONS

server_dir = os.path.dirname(__file__)
statics = os.path.join(os.path.split(server_dir)[0], "static")
templates = os.path.join(os.path.split(server_dir)[0], "templates")

app = Flask("note_14", static_folder=statics, template_folder=templates)

app.secret_key = SECRET_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS

login_manager = LoginManager(app)
login_manager.login_view = "user_login"

app.before_request(inject_session)
app.after_request(close_session)

from .users import login
from .controller import *
