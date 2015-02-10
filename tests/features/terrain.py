from lettuce import before, after, world
from splinter import Browser


@before.each_scenario
def initial_setup(server):
    world.browser = Browser()


@after.each_scenario
def cleanup(server):
    world.browser.quit()

