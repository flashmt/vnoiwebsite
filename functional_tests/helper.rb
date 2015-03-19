require 'capybara'
require 'capybara/dsl'
require 'capybara/rspec'
require 'capybara-screenshot'
require 'capybara-screenshot/rspec'
require 'pry'
require 'capybara/poltergeist'
require 'capybara-webkit'

RSpec.configure do |config|
  config.include Capybara::DSL, type: :feature
end

# By default, Capybara will try to boot a rack application, so we need to switch it off
Capybara.run_server = false
# The default driver is :rack_test, which does not support Javascript, so we need to switch to Selenium
Capybara.default_driver = :selenium
Capybara.default_selector = :css
if ENV.has_key?('TRAVIS_TEST_ENV')
  puts 'Use headless browser'
#  Capybara.register_driver :poltergeist do |app|
#    Capybara::Poltergeist::Driver.new(app, {
#      js_errors: false
#    })
#  end
  Capybara.javascript_driver = :webkit
end


# Set default wait time for page elements lookup to 5 seconds
Capybara.default_wait_time = 5
# HTML files & screenshots at failure points will be saved in output folder
Capybara.save_and_open_page_path = './output'
Capybara::Screenshot::RSpec.add_link_to_screenshot_for_failed_examples = true
Capybara::Screenshot::RSpec::REPORTERS['RSpec::Core::Formatters::HtmlFormatter'] = Capybara::Screenshot::RSpec::HtmlEmbedReporter

ROOT_URL = 'http://localhost:8000'

def verify_content(texts)
  texts.each { |text|
    puts "Looking for string '#{text}'"
    expect(page).to have_content(text)
  }
end

def random_string(length)
  (0...length).map { ('a'.ord + rand(26)).chr }.join
end

def login(user, password)
  puts 'Logging in...'
  click_on 'Sign in'
  fill_in 'id_username', with: user
  fill_in 'id_password', with: password
  if ENV.has_key?('TRAVIS_TEST_ENV')
    find('#login_submit').trigger(:click)
  else
    click_on 'Login'
  end
end

def register(username, email, password, password2: nil,
             last_name: 'Trung', first_name: 'Nguyen',
             dob: '23/06/1992')
  password2 ||= password
  puts "Register #{username}, #{email}, #{password}"

  visit "#{ROOT_URL}/user/register"
  within '#register_form' do
    fill_in 'id_username', with: username
    fill_in 'id_email', with: email
    fill_in 'id_last_name', with: last_name
    fill_in 'id_first_name', with: first_name
    fill_in 'id_dob', with: dob
    fill_in 'id_password1', with: password
    fill_in 'id_password2', with: password2
    click_on 'OK'
  end
end

def fill_in_ckeditor(locator, opts)
  content = opts.fetch(:with).to_json
  page.execute_script <<-SCRIPT
    CKEDITOR.instances['#{locator}'].setData(#{content});
    $('textarea##{locator}').text(#{content});
  SCRIPT
end

def verify_breadcrumbs(texts)
  within '#breadcrumbs' do
    texts.each do |text|
      puts "Checking breadcrumbs: #{text}"
      expect(page).to have_content(text)
    end
  end
end

def verify_flash_messages(texts)
  within '#flash-messages' do
    texts.each do |text|
      puts "Checking flash message: #{text}"
      expect(page).to have_content(text)
    end
  end
end

def browser_history_back
  page.evaluate_script('window.history.back()')
end
