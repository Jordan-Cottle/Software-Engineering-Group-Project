""" Package for database models.

All database models should be importable from this package directly.
The rest of the project shouldn't need to know about what specific file
a model comes from. Just that it is a model and comes from here.
"""

# pylint: disable=wrong-import-position,wrong-import-order

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


from .notes import Note, NoteSection
from .users import User
