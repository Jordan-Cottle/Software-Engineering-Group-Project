import pytest

import config

config.DB_FILENAME = f":memory:"

# Set up models in the in-memory db
from models import Base
from database import Session, ENGINE

from server import app

from database import create_note, create_user, get_user


@pytest.fixture(name="client")
def client_fixture():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(name="models", autouse=True)
def create_database_models():
    """ This ensures that every test has a clean database. """
    Base.metadata.create_all(ENGINE)

    yield None

    Base.metadata.drop_all(ENGINE)


@pytest.fixture(name="session")
def database_session():
    session = Session()
    yield session
    session.close()


@pytest.fixture(name="user")
def test_user(session):
    user = create_user(session, "Test", "1234")
    session.commit()
    return user


@pytest.fixture(name="other_user")
def test_other_user(session):
    other_user = create_user(session, "Other", "1234")
    session.commit()
    return other_user


@pytest.fixture(name="note")
def test_note(session, user):
    note = create_note(
        session,
        f"Test Note",
        f"Note is for tests only.\nThis should not be in the real database",
        user,
    )
    session.commit()

    return note


@pytest.fixture(name="notes")
def test_notes(session, user):
    notes = []
    for i in range(5):
        notes.append(
            create_note(
                session,
                f"Test Note {i}",
                f"Note {i} is for tests only.\nThis should not be in the real database",
                user,
            )
        )

    session.commit()

    return notes
