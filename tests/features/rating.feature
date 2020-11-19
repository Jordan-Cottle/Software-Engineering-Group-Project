Feature: rating
    In order to understand the quality of my notes
    As a user
    I want to rate other user's notes and users to rate mine

    Scenario: Bob rates Joe's note
        Given I am logged in as "Bob"
        And I am on the note detail page for "Joe's notes"
        And the note "Joe's Math Formulas" is "public"
        When I click on "Joe's Math Formulas" 
        Then I will be on "Joe's Math Formulas" note page.
        When I click on rate 
        Then I click the number 3
        When I click "Submit"
        Then Joe's note "Joe's Math Formulas" is rated by Bob

    Scenario: Bob tries to rate Joe's note after previously rating. 
        Given I am logged in as "Bob"
        And I am on the note detail page for "Joe's notes"
        And the note "Joe's Math Formulas" is "public"
        When I click on "Joe's Math Formulas" 
        Then I should be on "Joe's Math Formulas" note page.
        When I try to rate Joe's note
        Then I am unable to rate Joe, but see my previous rating.



    