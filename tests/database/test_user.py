from database import create_user


def test_create_user(session):
    user = create_user(session, name="Bob", password="1234")
    session.commit()

    assert user.name == "Bob", "Bob's name should not be changed"
    assert user.password != "1234", "User password should be protected by a hash!"
    assert user.id == 1, "Bob should have an id!"
