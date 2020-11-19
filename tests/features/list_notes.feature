Feature: List Notes
    In order to list my notes
    As a user
    I want to be able to view all of my notes as a list
    so I can see all the items I have posted

Scenario: Joe views notes as a list
        Given a user "Joe" exists
        And I am logged in as "Joe"
        And a note "How to Train My Dinosaur" by "Joe" exists
        And a note "Bank Heist Notes" by "Joe" exists
        When I go to the "Notes" page
        Then I should see "How to Train My Dinosaur"
        And I should see "Bank Heist Notes"
