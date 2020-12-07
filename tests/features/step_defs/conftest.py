""" This module contains common fixtures and setup for bdd style tests. """

from pytest_bdd import given, when, then
from pytest_bdd.parsers import parse

from database import create_user, create_note, get_user
from models import User, Note

TEST_PASSWORD = "123456789"


def find_note(session, note_title):
    """ Get the id of a note based on it's title. """

    notes = session.query(Note).all()

    for note in notes:
        if note.title == note_title:
            return note


class TestSession:
    """ Session for representing a user's session during a test. """

    def __init__(self, test_client) -> None:
        self.test_client = test_client
        self.response = None
        self.user = None

    def login(self, user):
        """ Log in a user. """

        self.post("/login", data={"user_name": user.name, "password": TEST_PASSWORD})
        self.user = user

    def get(self, *args, **kwargs):
        """ Submit a GET request to the server. """

        self.response = self.test_client.get(*args, **kwargs)
        return self.response

    def post(self, *args, **kwargs):
        """ Submit a POST request to the server. """

        self.response = self.test_client.post(*args, **kwargs)
        return self.response


@given(parse('a user "{user_name}" exists'))
def user_exists(session, user_name):
    user = create_user(session, user_name, TEST_PASSWORD)
    session.commit()

    return user


@given(parse('I am logged in as "{user_name}"'), target_fixture="test_session")
def login_user(session, client, user_name):
    print(*session.query(User).all())
    user = get_user(session, user_name)

    test_session = TestSession(client)
    test_session.login(user)

    return test_session


@given(parse('a note "{note_title}" by "{user_name}" exists'))
def note_exists(session, note_title, user_name):
    user = get_user(session, user_name)

    print(f"Creating {note_title}")
    note = create_note(session, note_title, "Default test note", user)
    session.commit()

    return note


@when(parse('I navigate to "{route}"'))
def request_route(test_session, route):
    test_session.get(route)


@when(parse('I navigate to the note detail page for "{note_title}"'))
def request_route(session, test_session, note_title):
    note = find_note(session, note_title)

    test_session.get(f"notes/{note.id}")


@then(parse('I should see "{text}"'))
def check_response(test_session, text):
    data = test_session.response.get_data(as_text=True)

    assert text in data, f"Response should contain {text}"


@then(parse('I should not see "{text}"'))
def check_response(test_session, text):
    data = test_session.response.get_data(as_text=True)

    assert text not in data, f"Response should not contain {text}"
