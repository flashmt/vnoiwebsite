Feature: Login
  User should be able to login to website

  Scenario: Login from Home page
    I go to url "/main"
    I see text "Login"
    I click on "Login"
    I login
    I see text "Welcome"

  Scenario: Login from Forum page
    I go to url "/forum"
    I see text "Login"
    I click on "Login"
    I login
    I see text "Welcome"
