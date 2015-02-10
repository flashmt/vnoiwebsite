from lettuce import world, step


@step(u'I login')
def admin_login(step):
    assert world.browser.is_text_present('Username')
    assert world.browser.is_text_present('Password')
    world.browser.find_by_css('#id_username').fill('admin')
    world.browser.find_by_css('#id_password').fill('admin')
    world.browser.find_by_xpath('//button[@class="btn btn-primary"]').first.click()
