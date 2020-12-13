"""
This module contains utilities for accessing comment data in the database

add_comment: Create a new comment in the database

get_comment: Get a single comment from the database

delete_comment: Delete a comment from the database
"""


from sqlalchemy.orm.exc import NoResultFound

from config import PermissionType
from models import Comment
from database import UnauthorizedError, check_permission, has_permission


def add_comment(session, text, note, user):
    """ adds comment to existing note in the database. """

    check_permission(session, PermissionType.COMMENT, user, note)

    comment = Comment(body=text, note_id=note.id, owner_id=user.id)

    session.add(comment)


def get_comment(session, comment_id, note, user):
    """ gets existing comment from the database """
    check_permission(session, PermissionType.READ, user, note)

    return session.query(Comment).filter_by(id=comment_id).one()


def delete_comment(session, comment_id, note, user):
    """ deletes comment on existing note from the database. """
    check_permission(session, PermissionType.ADMIN, user, note)
    comment = session.query(Comment).filter_by(id=comment_id).one()
    session.delete(comment)
