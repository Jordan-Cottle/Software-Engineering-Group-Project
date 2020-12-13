"""
This module contains utilities for accessing note data in the database

create_note: Create a new note in the database

get_note: Get a single note from the database

get_notes: Get all the notes from the database that a user can view
"""

import os
from datetime import date

from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename

from config import PermissionType
from models import Attachment, Note, NotePermission, NoteSection
from database import UnauthorizedError, add_permission, check_permission


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
    note = Note(title=title, created=date.today(), owner_id=user.id, views=0)
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

    check_permission(session, PermissionType.EDIT, user, note)

    session.delete(note)


def edit_note(session, title, text, note_id, user):
    """ edit an existing note in the database. """
    note = get_note(session, note_id, user)

    check_permission(session, PermissionType.EDIT, user, note)

    note.title = title
    note.text = text


def add_attachment(session, attachment, note, user):
    """Save and track attachment in the database.

    Parameters

    attachment -- A file retrieved from a flask request
        - See https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
    """

    check_permission(session, PermissionType.EDIT, user, note)

    # set file name
    name, ext = os.path.splitext(attachment.filename)

    # determine filename
    num = 1
    file_name = secure_filename(f"{user.name}_{name}_{num}.{ext}")
    while os.path.isfile(file_name):
        num += 1
        file_name = secure_filename(f"{user.name}_{name}_{num}.{ext}")

    # create model to track attachment
    attachment_model = Attachment(
        display_name=attachment.filename,
        file_name=file_name,
        note_id=note.id,
        owner_id=user.id,
    )
    session.add(attachment_model)

    # Flush to db to make sure everything is good
    session.flush()

    # finally save file to disk
    attachment.save(file_name)

    return attachment_model


def get_attachment(session, attachment_id, note, user):
    """ Retrieves attachment from database """
    check_permission(session, PermissionType.READ, user, note)
    attachment = session.query(Attachment).filter_by(id=attachment_id).one()

    return attachment


def delete_attachment(session, attachment_id, note, user):
    """ Deletes attachment from database """

    check_permission(session, PermissionType.EDIT, user, note)
    attachment = get_attachment(session, attachment_id, note, user)
    session.delete(attachment)
