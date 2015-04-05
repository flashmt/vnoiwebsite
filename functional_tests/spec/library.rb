require './helper.rb'
require './content/library.rb'

feature "Library" do
  before :each do
    hide_django_profile_bar
  end

  scenario "User should be able to view Library" do
    visit "#{ROOT_URL}/library"
    verify_content($library_index_content)
  end

  scenario "Only admin is able to add new article" do
    visit "#{ROOT_URL}/library"
    expect(page).to have_no_content $create_topic

    login('vnoiuser', 'vnoiuser')
    visit "#{ROOT_URL}/library"
    expect(page).to have_no_content $create_topic

    click_on 'Logout'
    expect(page).to have_content 'Sign in'
    login('admin', 'admin')
    visit "#{ROOT_URL}/library"
    expect(page).to have_content $create_topic
  end

  scenario "Only admin is able to edit / pin article" do
    visit "#{ROOT_URL}/library"
    click_on $CTDL
    click_on $PDS
    expect(page).to have_content $reply
    expect(page).to have_no_content $edit
    expect(page).to have_no_content $unpin

    login('vnoiuser', 'vnoiuser')
    visit "#{ROOT_URL}/library"
    click_on $CTDL
    click_on $PDS
    expect(page).to have_content $reply
    expect(page).to have_no_content $edit
    expect(page).to have_no_content $unpin

    click_on 'Logout'
    expect(page).to have_content('Sign in')
    login('admin', 'admin')
    visit "#{ROOT_URL}/library"
    click_on $CTDL
    click_on $PDS
    expect(page).to have_content $reply
    expect(page).to have_content $edit
    expect(page).to have_content $unpin
  end

  scenario "Breadcrumbs should show library" do
    # Library index
    visit "#{ROOT_URL}/library"
    login('admin', 'admin')
    verify_breadcrumbs($breadcrumbs[:index])

    # Library forum - CTDL
    click_on $CTDL
    verify_breadcrumbs($breadcrumbs[:CTDL])
    
    # Library topic - PDS
    click_on $PDS
    verify_breadcrumbs($breadcrumbs[:PDS])

    # Library topic - reply
    first(:link, $reply).click
    verify_breadcrumbs($breadcrumbs[:reply])

    # Library topic - edit
    browser_history_back
    first(:link, $edit).click
    verify_breadcrumbs($breadcrumbs[:edit])

    # Library - create new article
    visit "#{ROOT_URL}/library"
    click_on $create_topic
    verify_breadcrumbs($breadcrumbs[:create])
  end
end
