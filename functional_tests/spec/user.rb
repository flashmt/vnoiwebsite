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
     '/user/1'
    ].each do |path|
      visit "#{ROOT_URL}#{path}"
      login('admin', 'admin')
      expect(current_path.chomp('/')).to eq("#{path}")
      verify_flash_messages(['Welcome back, admin'])
      click_on $logout
    end
  end

  scenario "Logged in user should not be able to access login / register page", :js => true do
    visit "#{ROOT_URL}/main"
    login('admin', 'admin')

    visit "#{ROOT_URL}/user/login"
    expect(current_path.chomp('/')).to eq("/main")

    visit "#{ROOT_URL}/user/register"
    verify_flash_messages(['Invalid request'])
    expect(current_path.chomp('/')).to eq("/main")
  end

  scenario "User should be able to register", :js => true do
    username = random_string(10)
    email = random_string(10) + '@gmail.com'
    register(username, email, '12345')
    visit "#{ROOT_URL}/main"
    login(username, '12345')
    verify_flash_messages(['Welcome back'])
    click_on 'Logout'

    email2 = random_string(10) + '@gmail.com'
    register(username, email2, '123456')
    expect(page).to have_content('Tài khoản này đã được đăng ký')
    visit "#{ROOT_URL}/main"
    login(username, '123456')
    expect(page).to have_content('Login')

    username2 = random_string(10)
    register(username2, email, '123456')
    expect(page).to have_content('Email này đã được đăng ký')
    visit "#{ROOT_URL}/main"
    login(username2, '123456')
    expect(page).to have_content('Login')

    register(username2, email2, '12345', password2: '123456')
    expect(page).to have_content('Mật khẩu nhập lại không khớp')
    visit "#{ROOT_URL}/main"
    login(username2, '12345')
    expect(page).to have_content('Login')

    register(username2, email2, '12345')
    visit "#{ROOT_URL}/main"
    login(username2, '12345')
    verify_flash_messages(['Welcome back'])
  end

  scenario "User should be able to link Codeforces account", :js => true do
    # Login
    visit "#{ROOT_URL}/main"
    login('admin', 'admin')

    # Link CF account - try wrong password
    visit "#{ROOT_URL}/user/1"
    click_on 'Link Codeforces account'
    fill_in 'id_username', with: 'vnoi_info_001'
    fill_in 'id_password', with: 'test12345'
    click_on 'OK'
    expect(page).to have_content('Tài khoản hoặc mật khẩu không đúng')
    visit "#{ROOT_URL}/user/1"
    expect(page).to have_content('Link Codeforces account')

    # Link CF account - try correct password
    visit "#{ROOT_URL}/user/1"
    click_on 'Link Codeforces account'
    fill_in 'id_username', with: 'vnoi_info_001'
    fill_in 'id_password', with: 'test123'
    click_on 'OK'
    expect(page).to have_content('Codeforces: vnoi_info_001')

    # Unlink
    visit "#{ROOT_URL}/user/1"
    click_on 'Unlink Codeforces account'
    expect(page).to have_content('Link Codeforces account')
  end

  scenario "User should be able to link VOJ account", :js => true do
    # Login
    visit "#{ROOT_URL}/main"
    login('admin', 'admin')

    # Link VOJ account - wrong password
    visit "#{ROOT_URL}/user/1"
    click_on 'Link VOJ account'
    fill_in 'id_username', with: 'mrtrung'
    fill_in 'id_password', with: 'test12345'
    click_on 'OK'
    expect(page).to have_content('Tài khoản hoặc mật khẩu không đúng')
    visit "#{ROOT_URL}/user/1"
    expect(page).to have_content('Link VOJ account')

    # Link CF account - try correct password
    visit "#{ROOT_URL}/user/1"
    click_on 'Link VOJ account'
    fill_in 'id_username', with: 'mrtrung'
    fill_in 'id_password', with: 'test123'
    click_on 'OK'
    expect(page).to have_content('VOJ: mrtrung')

    # Unlink
    visit "#{ROOT_URL}/user/1"
    click_on 'Unlink VOJ account'
    expect(page).to have_content('Link VOJ account')
  end

  scenario "User should be able to add friend", :js => true do
    # Login
    visit "#{ROOT_URL}/main"
    login('admin', 'admin')
    
    # Add user as friend
    visit "#{ROOT_URL}/user/2"
    click_on 'Add friend'
    verify_flash_messages(['Friend successfully added'])
    
    # Check friend list
    click_on 'admin'
    click_on 'My friends'
    within '#body-container' do
      expect(page).to have_content('vnoiuser')
    end

    # Remove friend
    click_on 'vnoiuser'
    click_on 'Remove friend'
    verify_flash_messages(['Friend successfully removed'])

    # Check friend list
    click_on 'admin'
    click_on 'My friends'
    within '#body-container' do
      expect(page).to have_no_content('vnoiuser')
    end
  end
end

