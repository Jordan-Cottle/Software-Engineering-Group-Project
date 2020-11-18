Feature: User Sign Up
    In order to track my notes
    As a user
    I want to be able to sign up for an account

    Scenario: Joe Signs up for an account
        Given I am on the "register" page
        And I enter "Joe" as my name
        And I enter "abcdefg" as my password
        When I click "register"
        Then a new account for me is created
        And I should see "account created"
