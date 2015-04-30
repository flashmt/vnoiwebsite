# bundle exec rspec spec/forum/forum_list.rb

require './helper.rb'
require './pages/forum/forum_list'

include ForumListModule

feature 'Forum list' do
  before :each do
    hide_django_profile_bar
  end

  scenario 'User should see all forums', js: true do
    [true, false].each do |is_login|
      visit "#{ROOT_URL}/forum"
      login if is_login
      verify_forum_list_page
      logout if is_login
    end
  end
end
