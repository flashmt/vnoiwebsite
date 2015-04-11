require './helper.rb'
require './content/users.rb'

feature "User" do
  before :each do
    hide_django_profile_bar
  end

  scenario "Basic login and logout", :js => true do
    visit "#{ROOT_URL}"

    verify_content($login_content)
    login('admin', 'admin')
    verify_content($logout_content)
  end

  scenario "User should be redirected to previous page", :js => true do
    ['',
     '/problem/list',
     '/forum', '/forum/1', '/forum/1/1',
     '/user/1'
    ].each do |path|
      visit "#{ROOT_URL}#{path}"
      login('admin', 'admin')
      expect(current_path.chomp('/')).to eq("#{path}")
      verify_flash_messages(['Welcome back, admin'])
      logout()
    end

    visit "#{ROOT_URL}/user/login"
    login('admin', 'admin')
    expect(current_path.chomp('/')).to eq('')
    logout()

    visit "#{ROOT_URL}/user/register"
    login('admin', 'admin')
    expect(current_path.chomp('/')).to eq('')
    logout()
  end

  scenario "Logged in user should not be able to access login / register page", :js => true do
    visit "#{ROOT_URL}"
    login('admin', 'admin')

    visit "#{ROOT_URL}/user/login"
    expect(current_path.chomp('/')).to eq("")

    visit "#{ROOT_URL}/user/register"
    verify_flash_messages(['Invalid request'])
    expect(current_path.chomp('/')).to eq("")
  end

  scenario "User should be able to register", :js => true do
    username = random_string(10)
    email = random_string(10) + '@gmail.com'
    register(username, email, '12345')
    visit "#{ROOT_URL}"

    # Now, cannot login because account is not yet activated
    login(username, '12345', false)
    expect(current_path.chomp('/')).to eq('/user/login')

    # Activate account & login
    activate_account(username)
    login(username, '12345')
    verify_flash_messages(['Welcome back'])
    logout()

    email2 = random_string(10) + '@gmail.com'
    register(username, email2, '123456')
    expect(page).to have_content('Tài khoản này đã được đăng ký')
    visit "#{ROOT_URL}"
    login(username, '123456',false)
    expect(page).to have_content('Login')

    username2 = random_string(10)
    register(username2, email, '123456')
    expect(page).to have_content('Email này đã được đăng ký')
    visit "#{ROOT_URL}"
    login(username2, '123456', false)
    expect(page).to have_content('Login')

    register(username2, email2, '12345', password2: '123456')
    expect(page).to have_content('Mật khẩu nhập lại không khớp')
    visit "#{ROOT_URL}"
    login(username2, '12345', false)
    expect(page).to have_content('Login')

    register(username2, email2, '12345')
    activate_account(username2)
    visit "#{ROOT_URL}"
    login(username2, '12345')
    verify_flash_messages(['Welcome back'])

    click_on username2
    expect(page).to have_content(username2)
    verify_content($profile_content)
  end

  scenario "User should be able to link Codeforces account", :js => true do
    # Login
    visit "#{ROOT_URL}"
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
    visit "#{ROOT_URL}"
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
    visit "#{ROOT_URL}"
    login('admin', 'admin')
    
    # Add user as friend
    visit "#{ROOT_URL}/user/2"
    if page.has_text?($remove_friend_button)
      click_on $remove_friend_button
    end
    click_on $add_friend_button
    verify_flash_messages(['Friend successfully added'])
    
    # Check friend list
    click_on 'admin'
    click_on $friend_list
    within '#body-container' do
      expect(page).to have_content('vnoiuser')
    end

    # Remove friend
    click_on 'vnoiuser'
    click_on $remove_friend_button
    verify_flash_messages(['Friend successfully removed'])

    # Check friend list
    click_on 'admin'
    click_on $friend_list
    within '#body-container' do
      expect(page).to have_no_content('vnoiuser')
    end
  end

  scenario "User should be able to search friend", :js => true do
    visit "#{ROOT_URL}"
    login('admin', 'admin')
    visit "#{ROOT_URL}/user/1"
    click_on $friend_list

    # Search for vnoi
    fill_in 'id_user_prefix', with: 'vnoi'
    click_on 'OK'
    within '#body-container' do
      expect(page).to have_content('vnoiuser')
    end
    click_on 'vnoiuser'
    within '#body-container' do
      expect(page).to have_content('vnoiuser')
    end
    expect(current_path.chomp('/')).to eq('/user/2')

    # Search for abc
    visit "#{ROOT_URL}/user/1"
    click_on $friend_list
    fill_in 'id_user_prefix', with: 'abc'
    click_on 'OK'
    within '#body-container' do
      expect(page).to have_no_content('vnoiuser')
      expect(page).to have_content('Không có kết quả nào')
    end
  end

  scenario "User should be able to edit profile", :js => true do
    visit "#{ROOT_URL}"
    login('admin', 'admin')
    visit "#{ROOT_URL}/user/1"
    click_on $update_profile
    fill_in 'id_last_name', with: 'Admin - last name'
    fill_in 'id_first_name', with: 'Admin - first name'
    fill_in 'id_dob', with: '1992-06-23'
    click_on 'OK'

    expect(page).to have_content('Admin - last name Admin - first name')
    click_on $update_profile
    expect(find_field('id_last_name').value).to eq 'Admin - last name'
    expect(find_field('id_first_name').value).to eq 'Admin - first name'
  end
end

