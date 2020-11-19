Feature: rating
    In order to organize my notes
    As a user
    I want to organize my notes by views, rating, and alphabetically

    Scenario: Bob sorts "My Notes" alphabetically
        Given I am logged in as "Bob"
        And I am on the note detail page for "My Notes"
        When I click on "Sort"
        Then I prompted with "How do you want to sort?" 
        When I click on "alphabetically"
        Then the note detail page is sorted alphabetically
    
     Scenario: Bob sorts "My Notes" by rating
        Given I am logged in as "Bob"
        And I am on the note detail page for "My Notes"
        When I click on "Sort"
        Then I prompted with "How do you want to sort?" 
        When I click on "Rating"
        Then the note detail page is by rating highest to lowest

     Scenario: Bob sorts "My Notes" by views
        Given I am logged in as "Bob"
        And I am on the note detail page for "My Notes"
        When I click on "Sort"
        Then I prompted with "How do you want to sort?" 
        When I click on "Views"
        Then the note detail page is sorted by views highest to lowest