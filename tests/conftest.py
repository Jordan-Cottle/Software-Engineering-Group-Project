from unittest.mock import patch

import pytest
from models import Base
from server import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import create_note, create_user


@pytest.fixture(name="client")
def client_fixture():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(name="database")
def test_engine():
    engine = create_engine(f"sqlite:///:memory:")
    Base.metadata.create_all(engine)

    return engine


@pytest.fixture(name="session", autouse=True)
def database_session(database):
    Session = sessionmaker(bind=database)
    session = Session()

    with app.app_context():
        with patch("server.controller.g") as g_mock:
            g_mock.session = Session()
            yield session

    session.close()


@pytest.fixture(name="user")
def test_user(session):
    user = create_user(session, "Test", "1234")
    session.commit()
    return user


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
