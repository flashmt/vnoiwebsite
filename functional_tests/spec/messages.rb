require './helper.rb'
require './content/messages/messages.rb'

feature "Messages" do
  before :each do
    hide_django_profile_bar
  end

  def login_as_admin
    visit "#{ROOT_URL}"
    login('admin', 'admin')
    click_on $messages
  end

  def login_as_vnoiuser
    visit "#{ROOT_URL}"
    login('vnoiuser', 'vnoiuser')
    click_on $messages
  end

  scenario "User should not see Message URL until logged in", :js => true do
    visit "#{ROOT_URL}"

    expect(page).to have_no_content($messages)

    login('admin', 'admin')
    expect(page).to have_content($messages)

    click_on 'Logout'
    expect(page).to have_no_content($messages)
  end

  scenario "Path and breadcrumbs should be correct", :js => true do
    login_as_admin

    expect(current_path.chomp('/')).to eq("/message/inbox")
    verify_content($inbox_content)

    hash = { 'Hộp thư đến' => 'inbox', 
             'Thư đã gửi' => 'sent',
             'Viết thư mới' => 'write',
             'Thư đã lưu' => 'archives',
             'Thùng rác' => 'trash',
           }
    hash.each do |button, folder| 
      click_on(button)
      expect(current_path.chomp('/')).to eq("/message/#{folder}")
      verify_breadcrumbs(['Tin nhắn', button])    
    end
  end

  scenario "User should be directed to inbox", :js => true do
    login_as_admin
    
    click_on("Sender")
    puts current_path
    expect(current_path.chomp('/')).to eq("/message/inbox")

    click_on("Subject")
    expect(current_path.chomp('/')).to eq("/message/inbox")
  end

  scenario "Delete messages from inbox", :js => true do
    login_as_admin
    visit "#{ROOT_URL}/message/trash"
    expect(page).to have_content($messages_empty)

    visit("#{ROOT_URL}/message/inbox")
    check("message#1")
    check("message#2")
    click_on("Xóa")
    verify_content([$messages_empty])
    verify_flash_messages([$messages_deleted])
    
    visit "#{ROOT_URL}/message/trash"
    verify_content(['second letter', 'Hi admin'])
    check("message#1")
    check("message#2")
    click_on("Khôi phục")
    verify_content([$messages_empty])
    verify_flash_messages([$messages_recovered])

    visit("#{ROOT_URL}/message/inbox")
    verify_content(['second letter', 'Hi admin'])
  end

  scenario "Delete messages from sent", :js => true do
    login_as_admin

    visit("#{ROOT_URL}/message/sent")
    check("message#1")
    check("message#2")
    click_on("Xóa")
    verify_content([$messages_empty])
    verify_flash_messages([$messages_deleted])

    visit "#{ROOT_URL}/message/trash"
    verify_content(['second letter', 'Welcome'])
    check("message#1")
    check("message#2")
    click_on("Khôi phục")
    verify_content([$messages_empty])
    verify_flash_messages([$messages_recovered])    

    visit("#{ROOT_URL}/message/sent")
    verify_content(['second letter', 'Welcome'])
  end  

  scenario "Archive not empty after saving message", :js => true do
    login_as_admin
    visit "#{ROOT_URL}/message/archives"
    verify_content([$messages_empty])

    visit("#{ROOT_URL}/message/inbox")
    check("message#1")
    click_on("Lưu trữ")
    verify_flash_messages([$messages_archived])
    expect(page).to have_no_content('second letter')

    visit("#{ROOT_URL}/message/archives")    
    verify_content(['second letter'])

    init_database
  end

  scenario "User should be able to write and receive message", :js => true do
    login_as_admin
    visit "#{ROOT_URL}/message/write"

    within '#postman' do
      fill_in 'id_recipients', with: 'vnoiuser'
      fill_in 'id_subject', with: 'new message'
      click_on 'OK'
    end
    verify_flash_messages([$messages_sent])
    visit "#{ROOT_URL}/user/logout"
    login_as_vnoiuser
    visit("#{ROOT_URL}/message/inbox")    
    expect(page).to have_content('new message')

    init_database
  end

end
