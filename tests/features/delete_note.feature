Feature: Delete Note
    In order to manage unused notes
    As a user
    I want to delete a note

    Background:
        And a user "Joe" exists
        Given a note "Joe's Math Formulas" is owned by "Joe"

    Scenario: Joe deletes his note "Joe's Math Formulas"
        Given I am logged in as "Joe"
        And I am on the "notes page"
        And the link to "Joe's Math Formulas" is displayed
        When I click "delete" next to "Joe's Math Fomulas" link
        Then the note "Joe's Math Formulas" is deleted
