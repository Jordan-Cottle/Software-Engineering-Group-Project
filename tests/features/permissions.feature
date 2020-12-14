Feature: Private notes
    In order to keep my notes safe
    As a user
    I want to be able to control who can view my notes

    Background:
        Given a user "Joe" exists
        And a user "Susy" exists
        And a note "Spring 2021 courses" by "Joe" exists
        And a note "Susy's awesome recipe" by "Susy" exists

    Scenario: Joe views only his notes
        Given I am logged in as "Joe"
        When I navigate to "/notes"
        Then I should see "Spring 2021 courses"
        And I should not see "Susy's awesome recipe"

    Scenario: Susy tries to access a note she does not have access to
        Given I am logged in as "Susy"
        When I navigate to the note detail page for "Spring 2021 courses"
        Then I should be redirected to "/not_found"
        Then I should see "Resource not found"

    Scenario: Susy can view a private note she has been granted view access to
        Given I am logged in as "Susy"
        And "Susy" has been granted "read" permission for "Spring 2021 courses"
        When I navigate to the note detail page for "Spring 2021 courses"
        Then I should see "Spring 2021 courses"

    Scenario: Joe navigates to permission setting view
        Given I am logged in as "Joe"
        When I navigate to the note detail page for "Spring 2021 courses"
        And I click on "Set Permissions"
        Then I should see "User"
        And I should see "Admin"
        And I should see "Read"
        And I should see "Edit"
        And I should see "Comment"
        And I should see "new user"
        And I should see "Update Permissions"

