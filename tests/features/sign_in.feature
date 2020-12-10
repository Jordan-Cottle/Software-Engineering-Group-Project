Feature: User Sign In
    In order to view my notes
    As a user
    I want to be able to sign in to my account

    Scenario: Joe navigates to the login page
        When I navigate to "/login"
        Then I should see "Username"
        And I should see "Password"
        And I should see "Login"

    Scenario: Joe signs in to his account
        Given an account "Joe" with password "abcdefg" exists
        When I navigate to "/login"
        And I enter "Joe" for "user_name"
        And I enter "abcdefg" for "password"
        And I submit the form
        Then I should be logged in as "Joe"
        Then I should be redirected to "/"
        And I should see "Welcome back to the 49er Notes App, Joe!"
    
    Scenario: Joe fails to sign into his account
        Given an account "Joe" with password "abcdefg" exists
        When I navigate to "/login"
        And I enter "Joe" for "user_name"
        And I enter "12345" for "password"
        And I submit the form
        Then I should be redirected to "/login?error=401"
        And I should see "Your username or password was incorrect, please try again"

