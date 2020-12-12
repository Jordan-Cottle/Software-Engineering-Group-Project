import os
from unittest.mock import MagicMock

from config import PermissionType
from database import (
    get_note,
    get_notes,
    create_note,
    delete_note,
    create_rating,
    edit_note,
    add_attachment,
    add_permission,
    add_comment,
    get_comment,
    delete_comment,
)
from models import Note, Attachment, Comment


def test_add_comment(session, note, user):
    """ test adding comment """
    commentbody = "Wow comments wow"
    add_comment(session, commentbody, note.id, user)
    commentcount = session.query(Comment).filter_by(owner_id=user.id).count()

    assert commentcount == 1


def test_get_comment(session, note, user):
    add_comment(session, "hi", note.id, user)
    comment = session.query(Comment).filter_by(body="hi").one()
    comment2 = get_comment(session, comment.id)

    assert comment == comment2


def test_delete_comment(session, note, user):
    add_comment(session, "bye", note.id, user)
    comment = session.query(Comment).filter_by(body="bye").one()
    delete_comment(session, comment.id, user)
    count = session.query(Comment).count()
    assert count == 0
