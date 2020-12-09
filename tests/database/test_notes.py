from database import (
    get_note,
    get_notes,
    create_note,
    delete_note,
    create_rating,
    edit_note,
)
from models import Note


def test_create_simple_note(session, user):
    title = "Test Note"
    text = "This note is for a simple test"
    note = create_note(session, title, text, user)
    session.commit()

    assert note.id == 1, "New note should be the first one"
    assert note.title == title, "New note should have the specified title"
    assert note.text == text, "New note should have the specified text"
    assert note.owner == user.id, "Notes should be owned by their creators"


def test_create_multiline_note(session, user):
    title = "Test Note"
    text = "This note has\nmultiple lines."
    note = create_note(session, title, text, user)
    session.commit()

    assert note.id == 1, "New note should be the first one"
    assert note.title == title, "New note should have the specified title"
    assert note.text == text, "New note should have the specified text"
    assert note.owner == user.id, "Notes should be owned by their creators"

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
    before_delete = session.query(Note).filter(Note.owner == user.id).count()
    delete_note(session, note.id)
    after_delete = session.query(Note).filter(Note.owner == user.id).count()

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


def test_average_ratings(session, user, other_user, note):

    rating1 = create_rating(session, user, note, 1)

    rating2 = create_rating(session, other_user, note, 3)

    session.commit()

    assert note.rating == 2, "The note's rating should match 2"


def test_edit_note(session, user, note):
    edtitle = "This has been edited"
    edtext = "This has \n been edited"

    sections_before = len(note.sections)
    before_edit = session.query(Note).filter(Note.owner == user.id).count()
    edit_note(session, edtitle, edtext, note.id, user)
    after_edit = session.query(Note).filter(Note.owner == user.id).count()
    editednote = get_note(session, note.id, user)
    sections_after = len(editednote.sections)

    assert (
        before_edit == after_edit
    ), "Editing should not change number of notes in database"
    assert editednote.title == edtitle, "Editing note should change the title"
    assert editednote.text == edtext, "Editing note should change the text"
    assert sections_before == 2
    assert sections_after == 2
