""" Package for providing data to the application. """

import os
import json

from server import app

NOTES_PATH = os.path.join(app.root_path, "data", "notes")

with open(NOTES_PATH, "r") as note_file:
    NOTES = json.load(note_file)
