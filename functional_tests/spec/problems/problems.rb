# bundle exec rspec spec/problems/problems.rb

require './helper.rb'
require './pages/problems/problem_list.rb'

include ProblemListModule

feature 'Problem' do
  before :each do
    hide_django_profile_bar
  end

  scenario 'User should be able to see problem list', js: true do
    visit "#{ROOT_URL}/problems/list"
    verify_problem_list_page
  end
end
