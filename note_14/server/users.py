""" Module for managing user authentication. """

from http import HTTPStatus
from hashlib import sha256

from flask import g, redirect, url_for
from flask_login import login_user

from database import get_user, UserNotFound
from models import User as UserModel
from server import login_manager, app


class LoginError(Exception):
    """ A problem was encountered attempting to login. """

    status = HTTPStatus.UNAUTHORIZED


class InvalidPassword(LoginError):
    """ Indicates an invalid password was used to attempt a login. """


class User:
    """ Application level user class for managing authentication and authorization. """

    def __init__(self, user_name) -> None:

        self.user_name = user_name

        # User is not considered logged in by default
        self.authenticated = False

    @property
    def user(self):
        """ Get the user from the database. """
        return get_user(g.session, self.user_name)

    @classmethod
    def get(cls, session, user_id):
        """ Get an application user by their id. """

        user = session.query(UserModel).filter_by(id=user_id).one()

        return cls(user.name)

    def __getattr__(self, name):
        """ Delegate any access to attributes not defined here to the underlying database model. """

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

    def __str__(self) -> str:
        return self.user_name


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

    try:
        user.login(password)
    except UserNotFound as error:
        raise LoginError(f"Unable to locate {user} to login") from error

    USERS[user.id] = user

    # Notice flask-login of user login
    login_user(user)

    return user


@app.errorhandler(LoginError)
def send_to_login(error):
    """ Send user to login page. """

    return redirect(url_for("user_login", error=int(error.status)))
