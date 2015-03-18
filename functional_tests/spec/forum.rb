require './helper.rb'
require './content/forum/forum.rb'

feature "Forum" do
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
end

