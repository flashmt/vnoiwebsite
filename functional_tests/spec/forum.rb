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
    click_on 'Create new topic'

    title = random_string(10)
    content = random_string(50)

    fill_in 'id_title', with: title
    fill_in_ckeditor 'id_content', with: content
    click_on 'OK'

    expect(page).to have_content(title)
    expect(page).to have_content(content)

    expect(page).to have_content('Edit')
    expect(page).to have_content('Reply')
  end
end

