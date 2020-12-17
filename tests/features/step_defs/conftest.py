""" This module contains common fixtures and setup for bdd style tests. """
import re

import pytest
from pytest_bdd import given, then, when
from pytest_bdd.parsers import parse

from config import PermissionType
from database import add_permission, create_note, create_user, get_user
from models import Note

TEST_PASSWORD = "123456789"


def find_note(session, note_title):
    """ Get a note based on it's title. """

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

        self.form = {}

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


@pytest.fixture(name="test_session")
def test_session(client):
    """ Set up a TestSession to hold state between steps. """
    return TestSession(client)


@given(parse('a user "{user_name}" exists'))
def user_exists(session, user_name):
    user = create_user(session, user_name, TEST_PASSWORD)
    session.commit()

    return user


@given(parse('I am logged in as "{user_name}"'))
def login_user(session, test_session, user_name):
    user = get_user(session, user_name)

    test_session.login(user)

    return test_session


@given(parse('a note "{note_title}" by "{user_name}" exists'))
def note_exists(session, note_title, user_name):
    user = get_user(session, user_name)

    print(f"Creating {note_title}")
    note = create_note(session, note_title, "Default test note", user)
    session.commit()

    return note


PERMISSIONS = {
    "read": PermissionType.READ,
    "edit": PermissionType.EDIT,
    "comment": PermissionType.COMMENT,
    "admin": PermissionType.ADMIN,
}


@given(
    parse(
        '"{user_name}" has been granted "{permission_type}" permission for "{note_title}"'
    )
)
def grant_access(session, user_name, permission_type, note_title):
    """ Set up a permission for a user. """

    user = get_user(session, user_name)
    note = find_note(session, note_title)

    print(f'Adding "{permission_type}" permission for "{user_name}" on "{note_title}"')
    add_permission(
        session, PERMISSIONS[permission_type], user, note, triggered_by=note.owner
    )

    session.commit()


@when(parse('I navigate to "{route}"'))
def request_route(test_session, route):
    test_session.get(route)


@when(parse('I navigate to the note detail page for "{note_title}"'))
def request_route(session, test_session, note_title):
    note = find_note(session, note_title)

    test_session.get(f"notes/{note.id}")


@when(parse('I click on "{item}"'))
def click_on_item(test_session, item):
    html = test_session.response.get_data(as_text=True)
    link = f"{item}</a>" in html

    if link:
        match = re.search(f'<a.*href="([^"]+)".*>{item}</a>', html)
        assert match, f"Link labeled {item} not found in {html}"
        test_session.get(match.group(1))
        return

    assert False, f"{item} is not a link, test could not determine what to click on"


@when(parse('I enter "{value}" for "{field}"'))
def enter_form_data(test_session, value, field):
    test_session.form[field] = value


@when(parse("I submit the form"))
def enter_form_data(test_session):
    """ Detect form action and post data to it. """

    html = test_session.response.get_data(as_text=True)
    match = re.search(r'<form action="(/[^"]+)"', html)
    assert match, "Form must be located on the html page in order to submit it!"

    action = match.group(1)
    print(f'Form action: "{action}"')

    test_session.post(action, data=test_session.form)


@then(parse('I should see "{text}"'))
def check_response(test_session, text):
    data = test_session.response.get_data(as_text=True)

    assert text in data, f"Response should contain {text}."


@then(parse('I should not see "{text}"'))
def check_response(test_session, text):
    data = test_session.response.get_data(as_text=True)

    assert text not in data, f"Response should not contain {text}. {data}"


@then(parse('I should be redirected to "{url}"'))
def check_response(test_session, url):
    """ Assert an expected redirect and follow it. """

    html = test_session.response.get_data(as_text=True)

    assert "Redirecting..." in html, "Request should have triggered a redirect!"
    match = re.search(r'href="([^"]+)"', html)
    assert match, f"{html} should have a redirect url in it!"

    redirect_path = match.group(1)
    assert (
        redirect_path == url
    ), f"Test session should be redirected to {url}, found {redirect_path} instead"

    # Follow redirect for later steps to use
    test_session.get(redirect_path)
