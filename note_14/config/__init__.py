""" Package for providing secrets, configurable values and constants. """

from .secrets import *
from .permissions import PermissionType

DB_FILENAME = "note_14.db"
ECHO = False

UPLOAD_FOLDER = "/uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
