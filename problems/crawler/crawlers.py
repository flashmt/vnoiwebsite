# -*- coding: utf-8 -*-

import django
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

VOJ_BASE_URL = 'http://vn.spoj.com/'


def get_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return BeautifulSoup(response.text)


def get_elements_from_html(html, selector):
    if html is None:
        return None
    return html.select(selector)


def get_elements_from_url(url, selector):
    return get_elements_from_html(get_html(url), selector)


def get_category_url(category, page_id=0, problems_per_page=50):
    return '%sproblems/%s/sort=0,start=%d' % (VOJ_BASE_URL, category, page_id * problems_per_page)


def get_problem_url(problem_code):
    return '%sproblems/%s' % (VOJ_BASE_URL, problem_code)


def get_problems_from_category(category):
    result = []

    page_id = 0
    while True:

        if page_id >= 2:
            break

        problem_rows = get_elements_from_url(get_category_url(page_id=page_id), 'tr[class="problemrow"]')

        if problem_rows is None:
            break

        for problem_row in problem_rows:
            text = problem_row.__str__().replace('\n', ' ')
            matcher = PROBLEM_RE.match(text)

            if matcher:
                data = matcher.groupdict()
                problem_code = data['code']

                

                # problem = Problem(problem_code)
                # problem.fields['category'] = category.pk
                # problem.fields['problem_id'] = data['id']
                # problem.fields['name'] = data['name'].replace('ð', 'đ')

                # if category.fields['name'] == 'acm':
                #     problem.fields['accept_count'] = data['ac_count']
                #     problem.fields['accept_rate'] = data['ac_rate']
                #     problem.fields['score'] = round(80.0 / (40 + int(data['ac_count'])), 1)

                # result.append(problem)

        page_id += 1

    return result
