require './helper.rb'
require './content/users/login.rb'
require './content/users/logout.rb'

feature "User" do
  scenario "Basic login and logout", :js => true do
    visit "#{ROOT_URL}/main"

    verify_content($login_content)
    login('admin', 'admin')
    verify_content($logout_content)
  end

  scenario "User should be redirected to previous page", :js => true do
    ['/main',
     '/problem/list',
     '/forum', '/forum/1', '/forum/1/1',
     '/user/1'].each do |path|
      visit "#{ROOT_URL}#{path}"
      login('admin', 'admin')
      expect(current_path.chomp('/')).to eq("#{path}")
      click_on $logout
    end
  end
end
