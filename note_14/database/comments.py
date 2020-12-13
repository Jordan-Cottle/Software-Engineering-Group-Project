"""
This module contains utilities for accessing comment data in the database

add_comment: Create a new comment in the database

get_comment: Get a single comment from the database

delete_comment: Delete a comment from the database
"""


from sqlalchemy.orm.exc import NoResultFound

from config import PermissionType
from models import Comment
from database import UnauthorizedError, check_permission, get_note, has_permission


def add_comment(session, text, note, user):
    """ adds comment to existing note in the database. """

    check_permission(session, PermissionType.COMMENT, user, note)

    comment = Comment(body=text, note_id=note.id, owner_id=user.id)

    session.add(comment)


def get_comment(session, comment_id, user, note):
    """ gets existing comment from the database """
    if has_permission(session, PermissionType.READ, user, note):
        try:
            return session.query(Comment).filter_by(id=comment_id).one()
        except NoResultFound as error:
            raise UnauthorizedError(f"{comment_id} not found") from error


def delete_comment(session, comment_id, note, user):
    """ deletes comment on existing note from the database. """
    comment = get_comment(session, comment_id, user, note)
    if has_permission(session, PermissionType.ADMIN, user, note):
        session.delete(comment)
