from lettuce import world, step
from features.const import ROOT_URL
from features.helpers import random_string


@step(u'I create new topic')
def create_new_post(step):
    topic_title = 'Topic ' + random_string(6)
    topic_content = 'Content ' + random_string(20)
    world.browser.find_by_css('#id_content').fill(topic_content)
    world.browser.find_by_css('#id_title').fill(topic_title)
    world.browser.find_by_xpath('//button[@class="btn btn-primary"]').click()

    assert world.browser.is_text_present('Title: ' + topic_title)
    assert world.browser.is_text_present('Created by admin')
    assert world.browser.is_text_present('Created at')
    assert world.browser.is_text_present('Content: ' + topic_content)
    assert world.browser.is_text_present('Edit this post')
    assert world.browser.is_text_present('Comment this post')
    # TODO: verify topic exist