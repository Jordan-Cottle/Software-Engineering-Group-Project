"""
This module contains utilities for accessing note data in the database

create_note: Create a new note in the database

get_note: Get a single note from the database

get_notes: Get all the notes from the database
"""

from datetime import date

from data import EXISTS, Connection


def create_tables():
    """ Create the note tables. """
    with Connection() as connection:
        connection.execute(
            """
            CREATE TABLE notes(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                TITLE CHAR(64),
                TEXT CHAR(256),
                DATE CHAR(64)
            );"""
        )


DATE_FORMAT = "%B %d, %Y"


def today():
    """ Get today's date as a string. """
    return date.today().strftime(DATE_FORMAT)


def get_notes():
    """ Get all notes from the database. """
    with Connection() as connection:
        data = connection.execute("SELECT id, title, text, date FROM notes").fetchall()

    return [
        {"id": note[0], "title": note[1], "text": note[2], "date": note[3]}
        for note in data
    ]


def get_note(note_id):
    """ Get a single note from the database. """
    with Connection() as connection:
        note = connection.execute(
            f"SELECT id, title, text, date FROM notes WHERE id = {note_id}"
        ).fetchone()
    return {"id": note[0], "title": note[1], "text": note[2], "date": note[3]}


def create_note(title, text):
    """ Create a new note in the database. """
    with Connection() as connection:
        connection.execute(
            f"""
        INSERT INTO NOTES (title, text, date)
    VALUES ('{title}', '{text}', '{today()}');
        """
        )


if not EXISTS:
    create_tables()
    create_note("Test note 1", "This note is here for testing")
    create_note("Test note 2", "This note should be in a database")
