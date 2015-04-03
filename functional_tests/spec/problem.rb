require './helper.rb'
require './content/problems.rb'

feature "Problems" do
  before :each do
    hide_django_profile_bar
  end

  scenario "User should be able to view problem list" do
    visit "#{ROOT_URL}/problem/list"
    verify_content($problem_list_content)
  end

  scenario "Breadcrumbs should show Problems" do
    # Problem list
    visit "#{ROOT_URL}/problem/list"
    verify_breadcrumbs(['Danh sách bài tập'])

    # Problem show
    visit "#{ROOT_URL}/problem/show/CTAIN"
    verify_breadcrumbs(['Danh sách bài tập', 'CTAIN'])

    # Problem discuss
    visit "#{ROOT_URL}"
    login('admin', 'admin')
    visit "#{ROOT_URL}/problem/discuss/CTAIN"
    verify_breadcrumbs(['Danh sách bài tập', 'CTAIN', 'Thảo luận'])

    # Problem discuss create topic
    click_on $create_topic
    verify_breadcrumbs(['Danh sách bài tập', 'CTAIN', 'Create new topic'])
    # Now we create a new topic and then verity breadcrumbs in edit page & topic page
    title = random_string(10)
    fill_in 'id_title', with: title
    fill_in_ckeditor 'id_content', with: random_string(20)
    click_on 'OK'
    expect(page).to have_content(title)

    # Problem discuss show topic
    visit "#{ROOT_URL}/problem/discuss/CTAIN"
    click_on title
    verify_breadcrumbs(['Danh sách bài tập', 'CTAIN', title])

    # Problem discuss reply topic
    first(:link, $reply).click
    verify_breadcrumbs(['Danh sách bài tập', 'CTAIN', title, $reply])

    browser_history_back
    first(:link, $edit).click
    verify_breadcrumbs(['Danh sách bài tập', 'CTAIN', title, $edit])
  end
end
