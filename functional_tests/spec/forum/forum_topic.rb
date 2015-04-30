# bundle exec rspec spec/forum/forum_topic.rb

require './helper.rb'
Dir['./pages/forum/*.rb'].each { |f| require f }
require './pages/components/header.rb'

include TopicCreateModule

feature 'Forum' do
  before :each do
    hide_django_profile_bar
  end
  scenario 'Create, view, delete topic', js: true do
    # Login as vnoiuser, create topic
    visit "#{ROOT_URL}"
    login
    click_on Header.forum
    first(:link, ForumList.forum_groups[:contest][:forums][:cf]).click
    click_on ForumShow.create_topic
    title, content = create_topic

    verify_content [title, content]
    verify_content [TopicShow.reply, TopicShow.edit]

    topic_path = "#{ROOT_URL}#{current_path}"

    # Logout
    logout

    # Verify that topic shows up in Forum:
    visit "#{ROOT_URL}"
    click_on Header.forum
    first(:link, ForumList.forum_groups[:contest][:forums][:cf]).click
    verify_content title

    # Verify that topic shows up in Recent posts
    visit "#{ROOT_URL}"
    within '#recent_post' do
      expect(page).to have_content title
      expect(page).to have_content 'vnoiuser'
    end

    # Check topic again
    visit topic_path
    verify_content [title, content]
    verify_no_content [TopicShow.reply, TopicShow.edit]

    # Login as admin and delete topic
    visit topic_path
    login('admin', 'admin')
    verify_content [title, content]
    verify_content [TopicShow.reply, TopicShow.edit, TopicShow.delete]
    first(:link, TopicShow.delete).click
    click_on 'OK'

    # Verify that topic is deleted
    visit "#{ROOT_URL}"
    click_on Header.forum
    first(:link, ForumList.forum_groups[:contest][:forums][:cf]).click
    verify_no_content title
  end

  scenario 'Pin and unpin posts', js: true do
    # Login as vnoiuser, create topic
    visit "#{ROOT_URL}"
    login
    click_on Header.forum
    first(:link, ForumList.forum_groups[:contest][:forums][:cf]).click
    click_on ForumShow.create_topic
    title, content = create_topic

    verify_content [title, content]
    verify_content [TopicShow.reply, TopicShow.edit]
    verify_no_content [TopicShow.pin, TopicShow.unpin]

    topic_path = "#{ROOT_URL}#{current_path}"

    # Logout
    logout

    # Login as admin and pin topic
    visit topic_path
    login('admin', 'admin')
    verify_content [title, content]
    verify_content [TopicShow.reply, TopicShow.edit, TopicShow.delete]
    first(:link, TopicShow.pin).click

    # Verify that we have unpin link
    verify_content [title, content, TopicShow.reply, TopicShow.edit, TopicShow.delete, TopicShow.unpin]
    verify_flash_messages ['Chủ đề đã được ghim lên trang chủ']

    # Verify that the topic shows up on home page
    visit "#{ROOT_URL}"
    verify_content [title, content]

    # Now we unpin the post
    visit topic_path
    first(:link, TopicShow.unpin).click

    verify_content [title, content, TopicShow.reply, TopicShow.edit, TopicShow.delete, TopicShow.pin]
    verify_flash_messages ['Chủ đề đã được bỏ khỏi trang chủ']

    # Verify that the topic disappeared from home page
    visit "#{ROOT_URL}"
    # Note that we cannot check for no title, because the title still appears in "Recent posts"
    verify_no_content [content]

    # Remove this topic
    visit topic_path
    first(:link, TopicShow.delete).click
    click_on 'OK'

    # Now go to home page again and verify
    visit "#{ROOT_URL}"
    # Note that we cannot check for no title, because the title still appears in "Recent posts"
    verify_no_content [title, content]
  end
end
