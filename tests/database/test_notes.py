from database import get_note, get_notes, create_note, delete_note

from models import NoteSection, Note


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


def test_get_note(session, user):
    title = "Test Note"
    text = "This note has\nmultiple lines."
    note = create_note(session, title, text, user)
    session.commit()

    retrieved_note = get_note(session, note.id)

    assert retrieved_note.id == note.id, "Note retrieved should match one created"
    assert retrieved_note.title == note.title, "Note retrieved should match one created"
    assert retrieved_note.text == note.text, "Note retrieved should match one created"
    assert retrieved_note.owner == note.owner, "Note retrieved should match one created"


def test_get_notes(session, notes):

    retrieved_notes = get_notes(session)
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

def test_delete_note(session, user):
    title = "Delete this note"
    text = "This note will not exist"
    note = create_note(session, title, text, user)
    session.commit()
    
    test_filter_count = 1
    test_count = 0
    before_delete = session.query(Note).filter(Note.owner == user.id).count()
    delete_note(session, note.id)
    after_delete = session.query(Note).filter(Note.owner == user.id).count()

    assert test_filter_count == before_delete, "The filter count test and before delete should be 1"
    assert test_count != before_delete, "Test count should not equal before delete"
    assert test_count == after_delete, "The count should be 0"
    assert before_delete != after_delete, "Before delete should be 1 and after delete should be 0, so they're not equal."
