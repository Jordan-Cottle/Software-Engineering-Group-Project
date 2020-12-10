"""
This module contains permission utilities.

add_permission -- Used to add new permissions to users for notes.

remove_permission -- Used to remove permissions from users on notes.

has_permission -- Used to check permissions of a user on a note.
"""

from config import PermissionType
from models import NotePermission


class UnauthorizedError(Exception):
    """Raised when a user attempts an action they are not authorized for."""


def add_permission(session, permission_type: PermissionType, user, note):
    """Add permission to user for note.

    permission -- The PermissionType to add
    user -- The user to give permission to
    note -- The note to give permission for
    """

    permission = NotePermission(type=permission_type, user_id=user.id, note_id=note.id)

    session.add(permission)

    return permission


def remove_permission(session, permission_type: PermissionType, user, note):
    """Remove permission from user for note.

    permission -- The PermissionType to remove
    user -- The user to take permission from
    note -- The note to remove permission from
    """

    permission = (
        session.query(NotePermission)
        .filter_by(user_id=user.id, note_id=note.id, type=permission_type)
        .one()
    )

    session.delete(permission)


def has_permission(session, permission_type: PermissionType, user, note) -> bool:
    """Check permission of user for note.

    permission -- The PermissionType to check
    user -- The user to check permission of
    note -- The note to check permission for
    """

    return (
        session.query(NotePermission)
        .filter_by(user_id=user.id, note_id=note.id, type=permission_type)
        .count()
        == 1
    )
