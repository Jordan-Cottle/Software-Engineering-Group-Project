import re

from pytest_bdd import scenario, when, then
from pytest_bdd.parsers import parse

from config import PermissionType
from models import Note
from database import has_permission, get_user


@scenario("permissions.feature", "Joe views only his notes")
def test_list_notes():
    pass


@scenario(
    "permissions.feature", "Susy tries to access a note she does not have access to"
)
def test_list_notes_without_permission():
    pass


@scenario(
    "permissions.feature",
    "Susy can view a private note she has been granted view access to",
)
def test_list_notes_without_permission():
    pass


@scenario("permissions.feature", "Joe navigates to permission setting view")
def test_navigate_to_permission_view():
    pass


@scenario("permissions.feature", "Joe gives permission to Susy")
def test_give_permission():
    pass


@scenario("permissions.feature", "Joe updates multiple permissions")
def test_update_permissions():
    pass


@when(parse('I toggle the "{permission_name}" permission for "{user_name}"'))
def select_permission(test_session, permission_name, user_name):
    html = test_session.response.get_data(as_text=True)

    # Discover row in permission table
    match = re.search(
        r'<td><input .* name="user_(\d+)" value="(\d+)">' + f"{user_name}</td>", html
    )
    if not match:
        print(f"{user_name} not found in existing user section of permission form.")
        test_session.form[f"new_{permission_name}"] = "on"
    else:
        row_id = match.group(1)
        match = re.search(
            r'<input\s+type="checkbox"\s+name='
            + f'"{permission_name}_{row_id}"'
            + r'\s+checked="true"\s+>',
            html,
        )
        if not match:
            if user_name == "Susy":
                print(html)
            print(f"Setting {permission_name} for {user_name}")
            test_session.form[f"{permission_name}_{row_id}"] = "on"
        else:
            print(f"Unsetting {permission_name} for {user_name}")
            # This is just a flag for the submit step to use
            test_session.form[f"{permission_name}_{row_id}"] = "off"


@when(parse("I submit the permission form"))
def submit_permissions(test_session):
    html = test_session.response.get_data(as_text=True)

    matches = re.findall(
        r'<td><input .* name="user_(\d+)" value="(\d+)">(\w+)</td>', html
    )
    for match in matches:
        row_id, user_id, user_name = match
        print(row_id, user_id, user_name)
        test_session.form[f"user_{row_id}"] = user_id

        for permission in PermissionType:
            key = f"{permission.value}_{row_id}"

            match = re.search(
                r'<input\s+type="checkbox"\s+name="' + key + r'"\s+checked="true"\s+>',
                html,
            )
            if match and key not in test_session.form:
                print(f"Adding unchanged {key} to permission form")
                test_session.form[key] = "on"
            elif test_session.form.get(key) == "off":
                print(f"Removing {key} from permission form")
                test_session.form.pop(key)

    match = re.search(r'<form.*action="(/[^"]+)"', html)
    assert match, "Form must be located on the html page in order to submit it!"

    action = match.group(1)
    print(f'Submitting {test_session.form} to "{action}"')

    test_session.post(action, data=test_session.form)


@then(
    parse('"{user_name}" should have "{permission_name}" permission on "{note_title}"')
)
def check_permission(session, user_name, permission_name, note_title):
    user = get_user(session, name=user_name)
    note = session.query(Note).filter_by(title=note_title).one()

    for permission in PermissionType:
        if permission.value == permission_name:
            break
    else:
        assert False, f"{permission_name} is not a valid permission!"

    assert has_permission(
        session, permission, user, note
    ), f"{user_name} should have {permission_name} for {note_title}"


@then(
    parse(
        '"{user_name}" should not have "{permission_name}" permission on "{note_title}"'
    )
)
def check_no_permission(session, user_name, permission_name, note_title):
    user = get_user(session, name=user_name)
    note = session.query(Note).filter_by(title=note_title).one()

    for permission in PermissionType:
        if permission.value == permission_name:
            break
    else:
        assert False, f"{permission_name} is not a valid permission!"

    assert not has_permission(
        session, permission, user, note
    ), f"{user_name} should not have {permission_name} for {note_title}"
