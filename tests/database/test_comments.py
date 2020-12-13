"""Testing comment stuff"""

from database import (
    add_comment,
    get_comment,
    delete_comment,
)
from models import Comment


def test_add_comment(session, note, user):
    """ test adding comment """
    commentbody = "Wow comments wow"
    add_comment(session, commentbody, note, user)
    comment = session.query(Comment).filter_by(owner_id=user.id).one()
    commentcount = session.query(Comment).filter_by(owner_id=user.id).count()

    assert commentcount == 1
    assert comment.body == commentbody


def test_get_comment(session, note, user):
    """ test getting comment """
    add_comment(session, "hi", note, user)
    comment = session.query(Comment).filter_by(body="hi").one()
    comment2 = get_comment(session, comment.id, note, user)

    assert comment.body == comment2.body


def test_delete_comment(session, note, user):
    """ test deleting comment """
    add_comment(session, "bye", note, user)
    comment = session.query(Comment).filter_by(body="bye").one()
    delete_comment(session, comment.id, note, user)
    count = session.query(Comment).count()

    assert count == 0
