from lettuce import world, step

from features.const import ROOT_URL


@step(u'I see text "(.+)"')
def see_text(step, text):
    assert world.browser.is_text_present(text)

@step(u'I go to url "(.+)"')
def go_to_url(step, url):
    if not url.startswith('http'):
        url = ROOT_URL + url
    world.browser.visit(url)


@step(u'I click on "(.+)"')
def click_on(step, text):
    assert world.browser.is_text_present(text)
    world.browser.find_link_by_text(text).click()

