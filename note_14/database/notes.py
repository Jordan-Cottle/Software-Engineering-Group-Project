"""
This module contains utilities for accessing note data in the database

create_note: Create a new note in the database

get_note: Get a single note from the database

get_notes: Get all the notes from the database that a user can view
"""

from datetime import date

from models import Note, NoteSection


class UnauthorizedError(Exception):
    """Raised when a user attempts an action they are not authorized for."""


def get_notes(session, user):  # pylint: disable=unused-argument
    """ Get all notes from the database that a user can see. """

    notes = user.notes

    # TODO: Add notes that user has view permission for

    return notes


def get_note(session, note_id, user):  # pylint: disable=unused-argument
    """Get a single note from the database.

    Will report an error if the user is not authorized to view that note.
    """

    # TODO: Do a more explicit check using permissions once they are set up
    for note in user.notes:
        if note.id == note_id:
            return note

    raise UnauthorizedError(
        f"{user} not authorized to access {note_id} or it does not exist"
    )


def create_note(session, title, text, user):
    """ Create a new note in the database. """
    note = Note(title=title, created=date.today(), owner=user.id)
    session.add(note)

    for i, line in enumerate(text.split("\n")):
        note.sections.append(NoteSection(content=line, index=i))

    return note


def edit_note(session, title, text, note_id):
    note = session.query(Note).filter_by(id=note_id).one()
    note.title = title
    note.text = text
    session.add(note)


def delete_note(session, note_id):
    """ Delete a note from the database """
    note = session.query(Note).filter_by(id=note_id).one()
    session.delete(note)
