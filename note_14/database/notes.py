"""
This module contains utilities for accessing note data in the database

create_note: Create a new note in the database

get_note: Get a single note from the database

get_notes: Get all the notes from the database
"""

from datetime import date

from models import Note, NoteSection


DATE_FORMAT = "%B %d, %Y"


def get_notes(session):
    """ Get all notes from the database. """
    return session.query(Note).all()

def delete_note(session,note_id):
    """ Delete a note from the database """
    delete_note = session.query(Note).filter_by(id=note_id).one()
    session.delete(delete_note)
    session.commit()


def get_note(session, note_id):
    """ Get a single note from the database. """
    return session.query(Note).filter_by(id=note_id).one()


def create_note(session, title, text, user):
    """ Create a new note in the database. """
    note = Note(title=title, created=date.today(), owner=user.id)
    session.add(note)

    for i, line in enumerate(text.split("\n")):
        note.sections.append(NoteSection(content=line, index=i))

    return note
