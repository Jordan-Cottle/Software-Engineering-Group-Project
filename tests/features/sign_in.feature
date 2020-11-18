Feature: User Sign In
    In order to view my notes
    As a user
    I want to be able to sign in to my account

    Scenario: Joe Signs in to his account
        Given I am on the "login" page
        And an account "Joe" with password "abdcefg" exists
        And I enter "Joe" as my name
        And I enter "abcdefg" as my password
        When I click "login"
        Then I should be logged in to the system
        And I should see "Welcome back, Joe"
