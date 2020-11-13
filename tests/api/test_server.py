from server import app
from database import get_note, get_notes

from database.notes import DATE_FORMAT


def assert_nav_exists(page_data):

    assert "<h1>Navigation</h1>" in page_data
    assert '<li><a href="/">Home</a></li>' in page_data
    assert '<li><a href="/notes">Course notes</a></li>' in page_data


def test_main_page(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert_nav_exists(html)

    # Assert basic content is there
    assert "<h1>Welcome to the 49er Notes App!</h1>" in html
    assert "<h2>Use this site to maintain and organize your notes.</h2>" in html


def test_notes_page(client, notes):
    response = client.get("/notes")
    html = response.get_data(as_text=True)

    print(response.data)
    assert_nav_exists(html)

    assert "<h1>List of available notes</h1>" in html

    for note in notes:
        assert f'<li><a href="/notes/{note.id}">{note.title}</a></li>' in html


def test_note_page(client, notes):
    note = notes[0]
    response = client.get(f"/notes/{note.id}")
    html = response.get_data(as_text=True)

    assert_nav_exists(html)

    assert "<h1>Note Data</h1>" in html

    assert note.title in html
    assert note.text in html
    assert note.created.strftime(DATE_FORMAT) in html