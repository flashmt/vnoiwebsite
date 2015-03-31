# -*- coding: utf-8 -*-
import time
import re
import requests
import html5lib

from bs4 import BeautifulSoup
from problems.models import SpojProblem

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
    # Since the problem statement of SPOJ sometimes contains '&', '<' and '>', which are not valid in correct HTML,
    # we must use a lenient parser
    return BeautifulSoup(response.text, 'html5lib')


def get_elements_from_html(html, selector):
    if html is None:
        return None
    return html.select(selector)


def get_elements_from_url(url, selector):
    return get_elements_from_html(get_html(url), selector)


def get_category_url(category, page_id=0, problems_per_page=50):
    return '%sproblems/%s/sort=0,start=%d' % (VOJ_BASE_URL, category.name, page_id * problems_per_page)


def get_problem_url(problem_code):
    return '%sproblems/%s' % (VOJ_BASE_URL, problem_code)


def get_problem_rank_url(problem_code):
    return '%sranks/%s' % (VOJ_BASE_URL, problem_code)


# Return: problem statement in HTML
def get_problem_statement(problem_code):
    problem_url = get_problem_url(problem_code)
    soup = get_html(problem_url)

    # Remove Google +1 button
    soup.find("div", {"style": "position: absolute; right: 0px"}).decompose()

    # Remove Google ads
    soup.find("div", {"class": "aProblemTop"}).decompose()

    # Remove FB like button
    soup.find("div", {"class": "fb-like"}).decompose()

    soup.find("div", {"id": "ccontent"}).decompose()

    # Remove problem information (at the bottom)
    soup.find("table", {"class": "probleminfo"}).decompose()

    # problem statement
    prob_content = soup.find("div", {"class": "prob"})
    prob_content.find('table').decompose()
    return prob_content.prettify()


# Find available language for a problem
# Return: array of language code
def get_problem_languages(problem_code):
    problem_rank_url = get_problem_rank_url(problem_code)
    soup = get_html(problem_rank_url)
    div_langs = soup.find("small")
    div_langs = BeautifulSoup(div_langs.prettify())

    langs = []
    for lang in div_langs.find_all("a"):
        langs.append(lang.text.strip())
    return langs


def get_problem_codes_from_category(category):
    result = []

    page_id = 0
    while True:

        # For testing
        if page_id >= 1:
            break

        time.sleep(1)
        problem_rows = get_elements_from_url(get_category_url(category, page_id=page_id), 'tr[class="problemrow"]')

        if problem_rows is None:
            break

        for problem_row in problem_rows:
            text = problem_row.__str__().replace('\n', ' ')
            matcher = PROBLEM_RE.match(text)

            if matcher:
                data = matcher.groupdict()
                problem_code = data['code']
                print 'problem = %s' % problem_code

                problem = SpojProblem.objects.filter(code=problem_code)
                if len(problem) == 0:
                    problem = SpojProblem.objects.create(
                        code=problem_code,
                        problem_id=data['id'],
                        name=data['name'].replace('ð', 'đ'),
                        category=category
                    )
                    need_update_statement = True
                else:
                    need_update_statement = False
                    problem = problem[0]

                if need_update_statement:
                    problem.statement = get_problem_statement(problem_code)

                if category.name == 'acm':
                    problem.accept_count = data['ac_count']
                    problem.accept_rate = data['ac_rate']
                    problem.score = round(80.0 / (40 + int(data['ac_count'])), 1)

                problem.save()
                time.sleep(1)

                result.append(problem)
        page_id += 1

    return result
