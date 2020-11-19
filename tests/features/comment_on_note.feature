Feature: Comment on Note
    In order to express my opinion
    As a user
    I want to comment on a user's notes 

    Background:
        Given a user "Joe" exists
        And a user "Bob" exists
        And a note "Joe's Math Formulas" is owned by "Joe"
        And the note "Joe's Math Formulas" is "public"

    Scenario: Bob comments on Joe's note
        Given I am logged in as "Bob"
        And I am on the note detail page for "Joe's Math Formulas"" 
        When I click on "Comment"
        And I type in my comment, "Joe, your formulas stink"
        And I click "Submit"
        Then the note "Joe's Math Formulas" has my comment.
