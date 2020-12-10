from pytest_bdd import scenario, given, then
from pytest_bdd.parsers import parse

from flask_login import current_user

from database import create_user


@scenario("sign_in.feature", "Joe navigates to the login page")
def test_sign_in_page():
    pass


@scenario("sign_in.feature", "Joe signs in to his account")
def test_sign_in_function():
    pass


@scenario("sign_in.feature", "Joe fails to sign into his account")
def test_sign_in_fail():
    pass


@given(parse('an account "{user_name}" with password "{password}" exists'))
def user_exists(session, user_name, password):
    user = create_user(session, user_name, password)
    session.commit()

    return user


@then(parse('I should be logged in as "{user_name}"'))
def check_response(user_name):
    """ Assert an expected redirect and follow it. """

    assert (
        current_user.name == user_name
    ), f'Client should be logged in as "{user_name}"'
