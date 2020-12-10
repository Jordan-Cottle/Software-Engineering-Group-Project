""" Package for providing database access to the application. """
# pylint: disable=wrong-import-position

from sqlalchemy import create_engine

from config import DB_FILENAME, ECHO

ENGINE = create_engine(f"sqlite:///{DB_FILENAME}", echo=ECHO)

from .session import *

from .permissions import *
from .users import *
from .notes import *
from .ratings import *
