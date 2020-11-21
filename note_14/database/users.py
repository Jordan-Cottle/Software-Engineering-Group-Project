"""
Module for providing database functions involving users.
"""

import os
from hashlib import sha256

from models import User


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


def get_user(session, name):
    """Retrieve a user by their name from the database.

    This does not do any checks on the password/hash. Just getting a reference to this model
    should not be considered logging in.
    """

    user = session.query(User).filter_by(name=name).one()

    return user
