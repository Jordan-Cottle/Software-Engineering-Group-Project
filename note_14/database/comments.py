"""
This module contains utilities for accessing comment data in the database

add_comment: Create a new comment in the database

get_comment: Get a single comment from the database

delete_comment: Delete a comment from the database
"""


from sqlalchemy.orm.exc import NoResultFound

from config import PermissionType
from models import Comment
from database import UnauthorizedError, check_permission, get_note


def add_comment(session, text, note_id, user):
    """ adds comment to existing note in the database. """
    note = get_note(session, note_id, user)

    check_permission(session, PermissionType.COMMENT, user, note)

    comment = Comment(body=text, note_id=note_id, owner_id=user.id)

    session.add(comment)


def get_comment(session, comment_id):
    """ gets existing comment from the database """
    try:
        return session.query(Comment).filter_by(id=comment_id).one()
    except NoResultFound as error:
        raise UnauthorizedError(f"{comment_id} not found") from error


def delete_comment(session, comment_id, user):
    """ deletes comment on existing note from the database. """
    comment = get_comment(session, comment_id)
    if comment.owner_id == user.id:
        session.delete(comment)
