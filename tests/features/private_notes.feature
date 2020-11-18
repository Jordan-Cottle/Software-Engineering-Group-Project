Feature: Private notes
    In order to keep my notes safe
    As a user
    I want to be able to control who can view my notes

    Background:
        And a user "Joe" exists
        And a user "Susy" exists
        Given a note "Spring 2021 courses" owned by "Joe"

    Scenario: Joe sets a note to private
        Given I am logged in as "Joe"
        And I am on the note detail page for "Spring 2021 courses"
        And the note "Spring 2021 courses" is "public"
        When I click on "toggle visibility"
        Then the note "Spring 2021 courses" should be "private"
    
    Scenario: Susy tries to access a note she does not have access to
        Given the note "Spring 2021 courses" is "private"
        And I am logged in as "Susy"
        When I navigate to the note page "Spring 2021 courses"
        Then I should see "Note unavailable"
    
    Scenario: Joe gives access to Susy
        Given I am logged in as "Joe"
        And I am on the note detail page for "Spring 2021 courses"
        And the note "Spring 2021 courses" is "private"
        When I click on "grant access"
        Then I should see a form for user privileges
        When I enter "Susy" for the name
        And I select "view" for the priviledge
        And I press "grant"
        Then I should see "View access to spring 2021 courses granted to Susy"
        And "Susy" should have permission to view "Spring 2021 courses"
    
    Scenario: Susy can view a private note she has been granted view access to
        Given the note "Spring 2021 courses" is "private"
        And "Susy" has been granted "view" permission for "Spring 2021 courses"
        And I am logged in as "Susy"
        When I navigate to the note page "Spring 2021 courses"
        Then I should see "Spring 2021 courses"
