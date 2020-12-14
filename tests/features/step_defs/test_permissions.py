from pytest_bdd import scenario


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