require 'capybara'
require 'capybara/dsl'
require 'capybara/rspec'
require 'capybara-screenshot'
require 'capybara-screenshot/rspec'
require 'pry'
require 'capybara/poltergeist'
require 'capybara-webkit'

require './pages/components/header.rb'

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

Capybara.ignore_hidden_elements = true

ROOT_URL = 'http://localhost:8000'

# Check if the page contains all string in texts.
# texts can be either:
# - single string
# - array of string
# - hash (in this case, the values will be check)
def verify_content(texts)
  if texts.is_a? Array
    texts.each { |text|
      puts "Find string: '#{text}'"
      expect(page).to have_content(text)
    }
  elsif texts.is_a? Hash
    texts.each { |_, text|
      puts "Find string: '#{text}'"
      expect(page).to have_content(text)
    }
  elsif texts.is_a? String
    puts "Find string: '#{texts}'"
    expect(page).to have_content(texts)
  else
    puts "Method verify_content not support type #{texts.class}"
    exit 1
  end
end

# Fill in a form
# Form must be a hash, with:
# - Keys: the keys to identify the DOM elements
# - Values: the labels of the input (this string will be check to be visible)
# Values must be a hash, with:
# - Keys: same keys as form
# - Values: the values to fill in
def fill_form(form, values)
  form.each do |key, value|
    expect(page).to have_content(value)
    fill_in key, with: values[key]
  end
end

def login(username = 'vnoiuser', password = 'vnoiuser')
  puts "Login on #{current_path}"

  # For some unknown reason, within does not work when include this module
  # in another module. Hence we must declare navbar variable & use it everywhere.
  within '#navbar' do
    first(:link, Header.login).click
    fill_form Header.login_form, {username: username, password: password}
    find_button(Header.login).click

    expect(page).to have_content username
  end
end

def logout(username = 'vnoiuser')
  puts "Log out on #{current_path}"

  within '#navbar' do
    click_on username
    click_on Header.logout
  end
end

# Generate a random string of given length
def random_string(length)
  (0...length).map { ('a'.ord + rand(26)).chr }.join
end

def register(username, email, password, password2: nil,
              last_name: 'Trung', first_name: 'Nguyen',
              dob: '1992-06-23')
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

def hide_django_profile_bar
  visit "#{ROOT_URL}"
  click_on 'Hide'
end

def activate_account(username)
  # Use magic to get the activation key
  if ENV.has_key?('USE_VIRTUAL_ENV')
    activation_key = `cd #{`pwd`.chomp}/..; pwd; venv/bin/python -m vnoiusers.get_activation_key '#{username}'`.split[1]
  else
    activation_key = `cd #{`pwd`.chomp}/..; pwd; python -m vnoiusers.get_activation_key '#{username}'`.split[1]
  end
  puts "activation key = #{activation_key}"
  visit "#{ROOT_URL}/user/confirm/#{activation_key}"
  expect(page).to have_content('Sign in')
end

def init_database
  if ENV.has_key?('USE_VIRTUAL_ENV')
    init_file = 'init_database_travis.sh'
  else
    init_file = 'init_database.sh'
  end
  `"cd #{__dir__} && cd .. && ./#{init_file}"`
end
