Feature: Forum
  User should be able to use forum functions

  Scenario: Create new topic in "Thảo luận đề QG"
    I go to url "/user/login"
    I login
    I go to url "/forum/"
    I see text "Thảo luận đề QG"
    I click on "Thảo luận đề QG"
    I see text "Forum > Thảo luận đề QG"
    I click on "Create new topic"
    I see text "Content"
    I see text "Title"
    I create new topic
