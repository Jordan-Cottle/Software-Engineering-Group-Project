Feature: Sorting
    In order to organize my notes
    As a user
    I want to organize my notes by views, rating, and alphabetically

Background:
        And a user "Bob" exists

    Scenario: Bob sorts his notes alphabetically
        Given I am logged in as "Bob"
        And I am on the "notes page"
        When I click on the "letter A symbol"
        Then the note page is sorted alphabetically
    
     Scenario: Bob sorts his notes by rating
        Given I am logged in as "Bob"
        And I am on the "notes page"
        When I click on the "letter R symbol"
        Then the note page is by "rating"

     Scenario: Bob sorts his notes by views
        Given I am logged in as "Bob"
        And I am on the "notes page"
        When I click on the "letter V symbol"
        Then the note page is sorted by "views"