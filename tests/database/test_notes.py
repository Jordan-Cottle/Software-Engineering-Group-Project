import os
from unittest.mock import MagicMock
from config import PermissionType, UPLOAD_FOLDER

from database import (
    get_note,
    get_notes,
    create_note,
    delete_note,
    create_rating,
    get_rating,
    edit_note,
    add_attachment,
    add_permission,
    get_attachment,
    delete_attachment,
    create_user,
    add_comment,
)
from models import Note, Attachment, Rating, NotePermission, Comment


def test_create_simple_note(session, user):
    title = "Test Note"
    text = "This note is for a simple test"
    note = create_note(session, title, text, user)
    session.commit()

    assert note.id == 1, "New note should be the first one"
    assert note.title == title, "New note should have the specified title"
    assert note.text == text, "New note should have the specified text"
    assert note.owner_id == user.id, "Notes should be owned by their creators"


def test_create_multiline_note(session, user):
    title = "Test Note"
    text = "This note has\nmultiple lines."
    note = create_note(session, title, text, user)
    session.commit()

    assert note.id == 1, "New note should be the first one"
    assert note.title == title, "New note should have the specified title"
    assert note.text == text, "New note should have the specified text"
    assert note.owner_id == user.id, "Notes should be owned by their creators"

    assert len(note.sections) == 2, "Each line of a note should be it's own section"


def test_get_note(session, user, note):
    retrieved_note = get_note(session, note.id, user)

    assert retrieved_note.id == note.id, "Note retrieved should match one created"
    assert retrieved_note.title == note.title, "Note retrieved should match one created"
    assert retrieved_note.text == note.text, "Note retrieved should match one created"
    assert retrieved_note.owner == note.owner, "Note retrieved should match one created"


def test_get_notes(session, notes, user):

    retrieved_notes = get_notes(session, user)
    for note, retrieved_note in zip(notes, retrieved_notes):
        assert retrieved_note.id == note.id, "Note retrieved should match one created"
        assert (
            retrieved_note.title == note.title
        ), "Note retrieved should match one created"
        assert (
            retrieved_note.text == note.text
        ), "Note retrieved should match one created"
        assert (
            retrieved_note.owner == note.owner
        ), "Note retrieved should match one created"


def test_delete_note(session, user, note):
    before_delete = session.query(Note).filter(Note.owner_id == user.id).count()
    delete_note(session, note.id, user)
    after_delete = session.query(Note).filter(Note.owner_id == user.id).count()

    assert (
        before_delete > after_delete
    ), "Delete should reduce the number of notes in the database."
    assert (
        before_delete == after_delete + 1
    ), "There should be exactly one less note in the database"


def test_create_rating(session, user, note):

    rating = create_rating(session, user, note, 5)
    session.commit()

    assert rating.note_id == note.id, "Rating note ID should match note ID created"
    assert rating.owner_id == user.id, "Rating owner should match user's ID"
    assert rating.value == 5, "The value of rating should match the value of 5"


def test_get_rating(session, user, note):

    firstcheck = get_rating(session, user, note)
    create_rating(session, user, note, 5)
    secondcheck = get_rating(session, user, note)

    assert firstcheck is None
    assert secondcheck.value == 5
    assert secondcheck.owner_id == user.id
    assert secondcheck.note_id == note.id


def test_average_ratings(session, user, other_user, note):

    create_rating(session, user, note, 1)
    session.commit()

    add_permission(
        session, PermissionType.READ, other_user, note, triggered_by=note.owner
    )
    session.commit()

    create_rating(session, other_user, note, 3)
    session.commit()

    assert note.rating == 2, "The note's rating should match 2"


def test_edit_note(session, user, note):
    edtitle = "This has been edited"
    edtext = "This has \n been edited"

    sections_before = len(note.sections)
    before_edit = session.query(Note).filter(Note.owner_id == user.id).count()
    edit_note(session, edtitle, edtext, note.id, user)
    after_edit = session.query(Note).filter(Note.owner_id == user.id).count()
    editednote = get_note(session, note.id, user)
    sections_after = len(editednote.sections)

    assert (
        before_edit == after_edit
    ), "Editing should not change number of notes in database"
    assert editednote.title == edtitle, "Editing note should change the title"
    assert editednote.text == edtext, "Editing note should change the text"
    assert sections_before == 2
    assert sections_after == 2


def test_cascades_work(session, user, note):
    """ make sure all things related to a note are deleted when a note is deleted """
    user2 = create_user(session, "dafdsfas", "dfadsfdsaf")
    add_permission(session, PermissionType.READ, user2, note, triggered_by=user)
    add_comment(session, "fdsa", note, user)
    create_rating(session, user, note, 5)
    delete_note(session, note.id, user)
    permissioncheck = (
        session.query(NotePermission)
        .filter_by(user_id=user2.id, note_id=note.id)
        .first()
    )
    ratingcheck = (
        session.query(Rating).filter_by(owner_id=user.id, note_id=note.id).first()
    )
    commentcheck = (
        session.query(Comment).filter_by(owner_id=user.id, note_id=note.id).first()
    )

    assert permissioncheck is None
    assert ratingcheck is None
    assert commentcheck is None


def test_add_attachment(session, user, note):
    """ Test uploading an attachment. """

    display_name = "test_file.txt"
    name, ext = os.path.splitext(display_name)
    file_name = f"{user.name}_{name}_1{ext}"
    location = os.path.join(UPLOAD_FOLDER, file_name)
    attachment = MagicMock(filename=display_name)

    model = add_attachment(session, attachment, note, user)
    session.commit()

    attachment.save.assert_called_once()
    attachment.save.assert_called_with(location)

    assert (
        model.display_name == display_name
    ), f"Attachment should have the name the user provided: got {model.display_name}, expected {display_name}"
    assert (
        model.file_name == location
    ), f"Attachments should be given a predictable, unique filename: got {model.file_name}, expected {file_name}"

    attachment = session.query(Attachment).one()
    assert (
        attachment.owner == user
    ), "The new attachment should belong to the uploading user"
    assert (
        attachment.note == note
    ), "The new attachment should be associated with the note"


def test_delete_attachment(session, user, note, attachment):

    before_delete = session.query(Attachment).count()
    delete_attachment(session, attachment.id, user, note)
    after_delete = session.query(Attachment).count()

    assert (
        before_delete > after_delete
    ), "Delete should reduce the number of attachments in the database."
    assert (
        before_delete == after_delete + 1
    ), "There should be exactly one less attachment in the database"


def test_get_attachment(session, user, note, attachment):

    test = get_attachment(session, attachment.id, note, user)
    assert (
        attachment.display_name == test.display_name
    ), f"Model display name should have the same display name as the test."
    assert (
        attachment.file_name == test.file_name
    ), f"Model file name should have the same file name as the test."
    assert (
        user.id == test.owner_id
    ), f"The user id should be the same as the test user id."
    assert (
        note.id == test.note_id
    ), f"The note id should be the same as the test note id."
