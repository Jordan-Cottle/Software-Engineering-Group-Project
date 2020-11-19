Feature: comment on note
    In order to express my opinion
    As a user
    I want to comment on user's notes 

    Scenario: Bob comments Joe's note
        Given I am logged in as "Bob"
        And I am on the note detail page for "Joe's notes"
        And the note "Joe's Math Formulas" is "public"
        When I click on "Joe's Math Formulas" 
        Then I am on "Joe's Math Formulas" note page.
        When I click on "Comment"
        And I type in my comment, "Joe, your formulas stink"
        When I click "Submit"
        Then Joe's note "Joe's Math Formulas" has a comment by Bob.
