"""
This module contains utilities for managing database sessions.

Session is a `session_maker` connected to the configured database engine.

inject_session is a function that will set up `Session` instances for each flask request
as a before_request handler

close_session is a function that will commit and close the database session at the end of a request
"""

from flask import g
from sqlalchemy.orm import sessionmaker

from database import ENGINE

Session = sessionmaker(bind=ENGINE)


def inject_session():
    """ Add a session to the flask request context. """

    g.session = Session()


def close_session(response):
    """ Commit and close out a session at the end of a flask request. """

    try:
        g.session.commit()
    except Exception as error:
        print(f"An error with the database has ocurred: {error!r}")
        raise
    finally:
        g.session.close()

    return response
