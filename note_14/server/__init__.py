""" Initialization file for the server package.

The flask application object is created here and is available for import at the package level.
"""

# pylint: disable=wrong-import-position
from flask import Flask

app = Flask("note_14")

from .controller import *
