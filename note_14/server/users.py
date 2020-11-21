""" Module for managing user authentication. """

from hashlib import sha256

from database import get_user
from flask import g

from flask_login import login_user

from server import login_manager

from sqlalchemy.orm.exc import DetachedInstanceError


class InvalidPassword(Exception):
    """ Indicates an invalid password was used to attempt a login. """


class User:
    """ Application level user class for managing authentication and authorization. """

    def __init__(self, user_name) -> None:

        # Get database instance of this user
        self.user = get_user(g.session, user_name)

        # User is not considered logged in by default
        self.authenticated = False

    @classmethod
    def get(cls, user_id):
        """ Get an application user by their id. """

        user = g.session.query(User).filter_by(id=user_id).one()

        return cls(user.name)

    def __getattr__(self, name):
        """ Delegate any access to attributes not defined here to the underlying database model. """

        try:
            return getattr(self.user, name)
        except DetachedInstanceError:
            self.user = g.session.merge(self.user)
            return getattr(self.user, name)

    def login(self, password):
        """Process login operation.

        This method will take authenticate the user by matching the password provided with
        the hash stored in the database.
        """

        salt = bytes.fromhex(self.user.salt)

        hashed = sha256(salt + password.encode()).digest().hex()

        if hashed == self.user.password:
            self.authenticated = True
        else:
            raise InvalidPassword("Passwords did not match!")

    @property
    def is_active(self):
        """Check if this user has an active account.

        This application doesn't currently have support for inactive users.
        """

        return True

    @property
    def is_authenticated(self):
        """Check if this user instance has been authenticated yet.

        For a user to be authenticated they must successfully submit the appropriate password.
        """

        return self.authenticated

    @property
    def is_anonymous(self):
        """Check if this user is anonymous.

        This application doesn't currently have support for inactive users.
        """

        return False

    def get_id(self):
        """ Get the id of this user. """

        return self.user.id


# Global dict for keeping track of users seen by the server
USERS = {}


@login_manager.user_loader
def load_user(user_id):
    """ Load user by id. """

    try:
        return USERS[user_id]
    except KeyError:
        return None


def login(user_name, password):
    """ Use user_name and password to authenticate the user. """

    user = User(user_name)

    user.login(password)

    USERS[user.id] = user

    # Notice flask-login of user login
    login_user(user)

    return user
