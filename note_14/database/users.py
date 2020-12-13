"""
Module for providing database functions involving users.
"""

import os
from hashlib import sha256

from models import User
from sqlalchemy.orm.exc import NoResultFound


class UserNotFound(Exception):
    """ Error for when an attempt to find a user was unsuccessful. """


def create_user(session, name, password):
    """Create a new user in the database.

    The password is salted and hashed, so the value is not stored
    in plain text.
    """

    salt = os.urandom(32)
    hashed = sha256(salt + password.encode()).digest()

    user = User(name=name, password=hashed.hex(), salt=salt.hex())

    session.add(user)
    return user


def get_user(session, name=None, user_id=None):
    """Retrieve a user by their name from the database.

    This does not do any checks on the password/hash. Just getting a reference to this model
    should not be considered logging in.
    """

    try:
        if name is not None:
            user = session.query(User).filter_by(name=name).one()
        elif user_id is not None:
            user = session.query(User).filter_by(id=user_id).one()
        else:
            raise TypeError("get_user() requires either a name or a user_id")
    except NoResultFound as error:
        raise UserNotFound(f"User {name} does not exist") from error

    return user
