require './helper.rb'
require './content/problems.rb'

feature "Problems" do
  before :each do
    hide_django_profile_bar
  end

  scenario "User should be able to view problem list" do
    visit "#{ROOT_URL}/problem/list"
    verify_content($problem_list_content)
  end
end
