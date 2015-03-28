require './helper.rb'
require './content/forum/forum.rb'

feature "Forum" do
  before :each do
    hide_django_profile_bar
  end

  scenario "User should see all forums", :js => true do
    visit "#{ROOT_URL}/forum/"
    verify_content($forum_content)
  end

  scenario "User should be able to create topic after login", :js => true do
    visit "#{ROOT_URL}/forum/"
    login('admin', 'admin')
    visit "#{ROOT_URL}/forum/"
    verify_content($forum_content)

    click_on 'Codeforces'
    click_on $create_topic

    title = random_string(10)
    content = random_string(50)

    fill_in 'id_title', with: title
    fill_in_ckeditor 'id_content', with: content
    click_on 'OK'

    expect(page).to have_content(title)
    expect(page).to have_content(content)

    expect(page).to have_content($edit)
    expect(page).to have_content($reply)
  end

  scenario "User should see breadcrumbs", :js => true do
    visit "#{ROOT_URL}/forum/"
    login('admin', 'admin')

    visit "#{ROOT_URL}/forum/"
    verify_breadcrumbs(['Forum'])

    click_on 'Codeforces'
    verify_breadcrumbs(['Forum', 'Codeforces'])

    click_on $create_topic
    verify_breadcrumbs(['Forum', 'Codeforces', $create_topic])

    visit "#{ROOT_URL}/forum/"
    click_on 'Codeforces'
    topic_title = 'CF Round 294'
    click_on topic_title
    verify_breadcrumbs(['Forum', 'Codeforces', topic_title])

    first(:link, $reply).click
    verify_breadcrumbs(['Forum', 'Codeforces', topic_title, $reply])

    browser_history_back
    first(:link, $edit).click
    verify_breadcrumbs(['Forum', 'Codeforces', topic_title, $edit])
  end

  scenario "Admin should be able to pin/unpin post", :js => true do
    # Assumption: this post will always be pinned in fixture
    # Visit post 1, unpin it
    visit "#{ROOT_URL}/forum/1/1"
    login('admin', 'admin')
    click_on $unpin_button
    verify_flash_messages(['Chủ đề đã được bỏ khỏi trang chủ'])

    # Verify that it is no longer on home page
    visit "#{ROOT_URL}"
    expect(page).to have_no_selector('h2', text: 'CF Round 294')

    # Pin the post again
    visit "#{ROOT_URL}/forum/1/1"
    click_on $pin_button
    verify_flash_messages(['Chủ đề đã được ghim lên trang chủ'])
    
    # Verify that it is on home page again
    visit "#{ROOT_URL}"
    expect(page).to have_selector('h2', text: 'CF Round 294')
  end

  scenario "Normal user should not be able to pin/unpin post", :js => true do
    visit "#{ROOT_URL}/forum/1/1"
    expect(page).to have_no_content $pin_button
    expect(page).to have_no_content $unpin_button
    login('vnoiuser', 'vnoiuser')
    # By redirection rule, user should still be on same page
    # but still check to be sure
    expect(current_path.chomp('/')).to eq('/forum/1/1')
    expect(page).to have_no_content $pin_button
    expect(page).to have_no_content $unpin_button

    # TODO: add test case for user going directly to pin/unpin URL.
    # Currently the behaviour is not fixed, so need to do this after it is confirmed
  end
end

