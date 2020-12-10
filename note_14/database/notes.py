"""
This module contains utilities for accessing note data in the database

create_note: Create a new note in the database

get_note: Get a single note from the database

get_notes: Get all the notes from the database that a user can view
"""

from datetime import date

from sqlalchemy.orm.exc import NoResultFound

from config import PermissionType
from models import Note, NotePermission, NoteSection
from database import UnauthorizedError, add_permission, has_permission


def get_notes(session, user):  # pylint: disable=unused-argument
    """ Get all notes from the database that a user can see. """

    notes = [
        permission.note
        for permission in user.permissions
        if permission.type == PermissionType.READ
    ]

    return notes


def get_note(session, note_id, user):
    """Get a single note from the database.

    Will report an error if the user is not authorized to view that note.
    """

    try:
        return (
            session.query(NotePermission)
            .filter_by(user_id=user.id, note_id=note_id, type=PermissionType.READ)
            .one()
            .note
        )
    except NoResultFound as error:
        raise UnauthorizedError(
            f"{user} not authorized to access {note_id} or it does not exist"
        ) from error


def create_note(session, title, text, user):
    """ Create a new note in the database. """
    note = Note(title=title, created=date.today(), owner_id=user.id)
    session.add(note)

    for i, line in enumerate(text.split("\n")):
        note.sections.append(NoteSection(content=line, index=i))

    # Flush to get id for note to assign permissions
    session.flush()

    # Add all permissions for note since the user is the owner
    for permission in PermissionType:
        add_permission(session, permission, user, note)

    return note


def delete_note(session, note_id, user):
    """ Delete a note from the database """
    note = get_note(session, note_id, user)

    if not has_permission(session, PermissionType.EDIT, user, note):
        raise UnauthorizedError(f"{user} not authorized to delete {note}")

    session.delete(note)


def edit_note(session, title, text, note_id, user):
    """ edit an existing note in the database. """
    note = get_note(session, note_id, user)

    if not has_permission(session, PermissionType.EDIT, user, note):
        raise UnauthorizedError(f"{user} not authorized to delete {note}")

    note.title = title
    note.text = text
