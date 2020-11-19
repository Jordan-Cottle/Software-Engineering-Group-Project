Feature:  Rating
    In order to understand the quality of my notes
    As a user
    I want to rate other user's notes and users to rate my notes

   Background:
        And a user "Joe" exists
        And a user "Bob" exists
        Given a note "Joe's Math Formulas" is owned by "Joe"
        Given the note "Joe's Math Formulas" is "public"

    Scenario: Bob rates Joe's note
        Given I am logged in as "Bob"
        And I am on the note detail page for "Joe's Math Formulas"
        When I click the third star
        Then the note "Joe's Math Formulas" has my 3 star rating

    Scenario: Bob tries to rate Joe's note after previously rating. 
        Given I am logged in as "Bob"
        Given I have already rated Joe's note
        And I am on the note detail page for "Joe's Math Formulas"
        When I click the second star
        Then the note "Joe's Math Formulas" has my updated 2 star rating



    