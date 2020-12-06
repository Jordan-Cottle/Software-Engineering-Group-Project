""" Package for providing database access to the application. """
# pylint: disable=wrong-import-position

from sqlalchemy import create_engine


DB_FILENAME = "note14.db"
ENGINE = create_engine(f"sqlite:///{DB_FILENAME}", echo=True)

from .session import Session, inject_session, close_session

from .users import create_user
from .notes import get_note, get_notes, create_note, delete_note
