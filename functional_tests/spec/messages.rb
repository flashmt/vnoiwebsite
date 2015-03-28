require './helper.rb'

feature "Messages" do
  before :each do
    hide_django_profile_bar
  end

  scenario "User should not see Message URL until logged in", :js => true do
    visit "#{ROOT_URL}"

    message_url_text = 'Messages'
    expect(page).to have_no_content(message_url_text)

    login('admin', 'admin')
    expect(page).to have_content(message_url_text)

    click_on 'Logout'
    expect(page).to have_no_content(message_url_text)
  end

  scenario "User should be directed to inbox", :js => true do
  	visit "{ROOT_URL}/main"

  	login('admin', 'admin')
  	
  end
end
