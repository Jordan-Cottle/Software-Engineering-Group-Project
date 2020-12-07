from pytest_bdd import scenario, given
from pytest_bdd.parsers import parse

from database import get_user, create_note


@scenario("list_notes.feature", "Joe views notes as a list")
def test_list_notes():
    pass


@scenario("note_detail.feature", "Joe views one of his notes")
def test_note_detail():
    pass


@given(parse('a note "{note_title}" by "{user_name}" exists with content "{content}"'))
def create_note_with_content(session, note_title, user_name, content):
    user = get_user(session, user_name)

    print(f"Creating {note_title}")
    note = create_note(session, note_title, content, user)
    session.commit()

    return note
