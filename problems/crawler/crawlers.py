# -*- coding: utf-8 -*-

import re
import requests
import sys
from bs4 import BeautifulSoup
from problems.crawler.models import Problem

PROBLEM_RE = re.compile(
    r'<tr class="problemrow">'
    r'.*<td>(?P<id>\d+)</td>'
    r'.*'
    r'<a href="/problems/(?P<code>[A-Z][A-Z0-9_]{1,7})/">'
    r'.*<b>(?P<name>.*?)</b>'
    r'.*<a href="/ranks/.*?>(?P<ac_count>\d+)</a>'
    r'.*<a href="/status/.*?>(?P<ac_rate>[\d\.]+)</a>'
)


def get_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        print 'Error crawling url: %s' % url
        sys.exit(0)
    return BeautifulSoup(response.text)


def get_elements_from_html(html, selector):
    return html.select(selector)


def get_elements_from_url(url, selector):
    return get_elements_from_html(get_html(url), selector)


def get_problems_from_category(category):
    problem_rows = get_elements_from_url(category.get_url(), 'tr[class="problemrow"]')
    result = []
    for problem_row in problem_rows:
        text = problem_row.__str__().replace('\n', ' ')
        matcher = PROBLEM_RE.match(text)

        if matcher:
            data = matcher.groupdict()
            problem_code = data['code']
            problem = Problem(problem_code)
            problem.fields['category'] = category.pk
            problem.fields['problem_id'] = data['id']
            problem.fields['name'] = data['name'].replace('ð', 'đ')

            if category.fields['name'] == 'acm':
                problem.fields['accept_count'] = data['ac_count']
                problem.fields['accept_rate'] = data['ac_rate']
                problem.fields['score'] = round(80.0 / (40 + int(data['ac_count'])), 2)

            result.append(problem)
            if problem_code == 'CTAIN':
                print data
                print problem.fields
    return result