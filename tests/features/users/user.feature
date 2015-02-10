Feature: Login
  User should be able to login to website

  Scenario: Login from home page
    I go to url "http://127.0.0.1:8000/main"
    I see text "Login"
    I click on "Login"
    I login
    I see text "Welcome"
