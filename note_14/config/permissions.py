""" This module contains an enum for different permission types. """

from enum import Enum


class PermissionType(str, Enum):
    """Enum for the different types of permissions.

    READ -- Allows for viewing a note

    EDIT -- Allow making edits to a note, including adding attachments and deleting

    COMMENT -- Allow a user to make comments on a note

    ADMIN -- Allow user to edit permissions on a note
    """

    ADMIN = "admin"
    READ = "read"
    EDIT = "edit"
    COMMENT = "comment"
