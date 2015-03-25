# -*- coding: utf-8 -*-
import re
import requests

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
    return BeautifulSoup(response.text)


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


def get_problem_statement(problem_code):
    problem_url = "%sproblems/%s" % (VOJ_BASE_URL, problem_code)
    soup = get_html(problem_url)

    # problem statement
    prob_content = soup.find("div", {"class": "prob"})
    # gg+ ads
    div_gg_ads = soup.find("div", {"style": "position: absolute; right: 0px"})
    # fb ads
    div_fb_ads = soup.find("div", {"class": "aProblemTop"})
    # problem info
    tab_prob_info = soup.find("table", {"class": "probleminfo"})
    # comments
    ccontent = soup.find("div", {"id": "ccontent"})

    prob_statement = prob_content.text

    # remove redundant sections
    prob_statement.replace(div_fb_ads.text, "")
    prob_statement.replace(div_gg_ads.text, "")
    prob_statement.replace(tab_prob_info.text, "")
    prob_statement.replace(ccontent.text, "")

    return prob_statement


def get_problem_codes_from_category(category):
    result = []

    page_id = 0
    while True:

        # For testing
        if page_id >= 1:
            break

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

                result.append(problem)
        page_id += 1

    return result
