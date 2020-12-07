Feature:  Rating
    In order to understand the quality of my notes
    As a user
    I want to rate other user's notes and users to rate my notes

   Background:
        Given a user "Joe" exists
        And a user "Bob" exists
        And a note "Joe's Math Formulas" by "Joe" exists
        And the note "Joe's Math Formulas" is "public"

    Scenario: Bob rates Joe's note
        Given I am logged in as "Bob"
        And I am on the note detail page for "Joe's Math Formulas"
        When I click star number "3"
        Then the note "Joe's Math Formulas" has my 3 star rating

    Scenario: Bob tries to rate Joe's note after previously rating. 
        Given I am logged in as "Bob"
        And I have already rated Joe's note
        And I am on the note detail page for "Joe's Math Formulas"
        When I click star number "2"
        Then the note "Joe's Math Formulas" has my updated "2" star rating



    