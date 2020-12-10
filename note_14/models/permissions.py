""" Module for defining permission related models. """

from models import Base
from sqlalchemy import Column, Integer, ForeignKey, Enum
from config import PermissionType


class NotePermission(Base):
    """Table for tracking user permissions on notes.

    This is essentially a many-to-many link table with a piece of meta data.

    note_id -- A FK to the note the permission is being set for
    user_id -- A FK to the user the permission is being assigned to

    type -- A PermissionType to allow certain actions on the specified note by the specified user
    """

    __tablename__ = "note_permissions"

    note_id = Column(Integer, ForeignKey("note.note_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    type = Column(Enum(PermissionType), primary_key=True)

    def __str__(self) -> str:
        return f"{self.user.name} has {self.type} permission on {self.note.title}"

    def __repr__(self) -> str:
        return f"NotePermission(type={self.type}, user_id={self.user_id}, note_id={self.note_id})"
