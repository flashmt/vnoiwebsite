# bundle exec rspec spec/general/auth.rb

require './helper.rb'
require './pages/components/header.rb'


feature 'Authentication' do
  before :each do
    hide_django_profile_bar
  end

  scenario 'User should be able to login and logout from every page', js: true do
    [
      '',
      'problems/list', 'problems/show/ROADS', 'problems/submit/ROADS', 'problems/status/ROADS/', 'problems/rank/ROADS/', 'problems/discuss/ROADS/',
      'forum', 'forum/1', 'forum/1/2/', 'forum/1/topic_create',
      'library', 'library/8/3/'
    ].each do |url|
      visit "#{ROOT_URL}/#{url}"
      login
      logout
    end
  end
end
