# bundle exec rspec spec/general/breadcrumbs.rb

require './helper.rb'
require './pages/components/header.rb'
require './pages/components/breadcrumbs.rb'

include BreadcrumbsModule


feature 'Breadcrumbs' do

  before :each do
    hide_django_profile_bar
  end

  scenario 'Breadcrumbs should show correctly for pages', js: true do
    # First, we check links that are accessible without need to login
    %w(
        problems/list/ problems/show/CTAIN problems/status/LAZYCOWS problems/rank/ROADS
        forum forum/1
        library/8/ library/8/3/
    ).each do |url|
      visit "#{ROOT_URL}/#{url}"
      verify_breadcrumbs

      login
      verify_breadcrumbs
      logout
    end

    # Then check for links that are only accessible when logged in
    %w(
      problems/submit/ROADS problems/discuss/LAZYCOWS
      forum/1/topic_create forum/8/topic_create
    ).each do |url|
      visit "#{ROOT_URL}"
      login
      visit "#{ROOT_URL}/#{url}"
      verify_breadcrumbs
      logout
    end

    # Links that are accessible only by admin
    %w(
      forum/8/topic_create/
    ).each do |url|
      visit "#{ROOT_URL}"
      login('admin', 'admin')
      visit "#{ROOT_URL}/#{url}"
      verify_breadcrumbs
      logout 'admin'
    end
  end
end
