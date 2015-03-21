require './helper.rb'
require './content/home.rb'
require './content/users/login.rb'

feature "Homepage" do
  before :each do
    hide_django_profile_bar
  end

  scenario "Go to homepage and look around", :js => true do
    visit "#{ROOT_URL}/main"

    verify_content($home_content)
    verify_content($login_content)
  end
end
