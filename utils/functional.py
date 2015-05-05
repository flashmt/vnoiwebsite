# -*- coding: utf-8 -*-
import time
import re
import requests
import dateutil.parser
import copy
import json
import sys
import os
import codecs
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    # Since the problem statement of SPOJ sometimes contains '&', '<' and '>', which are not valid in correct HTML,
    # we must use a lenient parser
    return BeautifulSoup(response.content.decode('utf-8', 'ignore').replace(u'ð', u'đ'), 'html5lib')


def get_elements_from_html(html, selector):
    if html is None:
        return None
    return html.select(selector)


def get_elements_from_url(url, selector):
    return get_elements_from_html(get_html(url), selector)


def url_exists(url):
    response = requests.get(url)
    if response.status_code != 200:
        return False
    if response.url != url:
        return False
    return True
