import pytest
from unittest.mock import patch

from server import app
from data import get_note, get_notes


@pytest.fixture(name="client")
def client_fixture():
    with app.test_client() as client:
        yield client


def assert_nav_exists(page_data):

    assert b"<h1>Navigation</h1>" in page_data
    assert b'<li><a href="/">Home</a></li>' in page_data
    assert b'<li><a href="/notes">Course notes</a></li>' in page_data


def test_main_page(client):
    response = client.get("/")
    html = response.data

    assert_nav_exists(html)

    # Assert basic content is there
    assert b"<h1>Welcome to the 49er Notes App!</h1>" in html
    assert b"<h2>Use this site to maintain and organize your notes.</h2>" in html


def test_notes_page(client):
    response = client.get("/notes")
    html = response.data

    print(response.data)
    assert_nav_exists(html)

    assert b"<h1>List of available notes</h1>" in html

    for note in get_notes():
        assert (
            f'<li><a href="/notes/{note["id"]}">{note["title"]}</a></li>'.encode()
            in html
        )


def test_note_page(client):
    note = get_note(1)
    response = client.get(f"/notes/{note['id']}")
    html = response.data

    assert_nav_exists(html)

    assert b"<h1>Note Data</h1>" in html

    assert note["title"].encode() in html
    assert note["text"].encode() in html
    assert note["date"].encode() in html