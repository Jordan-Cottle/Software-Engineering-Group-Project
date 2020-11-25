""" Deprecated tests.

The tests in this module are functional in nature and should be replaced by equivalent Gherkin style tests.
"""


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
