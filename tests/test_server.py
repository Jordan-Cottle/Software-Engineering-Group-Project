import pytest

from server import app


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

    assert_nav_exists(response.data)

    # Assert basic content is there
    assert b"<h1>Welcome to the 49er Notes App!</h1>" in response.data
    assert b"<h2>Use this site to maintain and organize your notes.</h2>" in response.data
