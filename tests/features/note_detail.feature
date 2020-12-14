Feature: View Note
    In order to use my notes
    As a user
    I want to be able to view the notes I have made in detail

Scenario: Joe views one of his notes
        Given a user "Joe" exists
        And I am logged in as "Joe"
        And a note "How to Train My Dinosaur" by "Joe" exists with content "Dinosaurs like to eat meat."
        When I navigate to the note detail page for "How to Train My Dinosaur"
        Then I should see "How to Train My Dinosaur"
        And I should see "Dinosaurs like to eat meat."
