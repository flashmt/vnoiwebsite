# -*- coding: utf-8 -*-
import time
import re
import requests
import html5lib
import dateutil.parser
import copy
import json
import sys
import os
import codecs

from bs4 import BeautifulSoup
from problems.models import SpojProblem
from problems.models import SpojProblemLanguage


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
# this url is used to get all languages
VOJ_TEST_URL = 'http://vn.spoj.com/submit/TEST/'


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


def get_category_url(category, page_id=0, problems_per_page=50):
    return '%sproblems/%s/sort=0,start=%d' % (VOJ_BASE_URL, category.name, page_id * problems_per_page)


def get_problem_url(problem_code):
    return '%sproblems/%s' % (VOJ_BASE_URL, problem_code)


def get_problem_rank_url(problem_code):
    return '%sranks/%s' % (VOJ_BASE_URL, problem_code)


def get_problem_submit_url(problem_code):
    return '%ssubmit/%s' % (VOJ_BASE_URL, problem_code)


def get_contest_rank_url(contest_id):
    return '%s%s/ranks' % (VOJ_BASE_URL, contest_id)


def get_problem_html(problem_code):
    return get_html(get_problem_url(problem_code))


def get_problem_rank_html(problem_code):
    return get_html(get_problem_rank_url(problem_code))


def get_contest_rank_html(contest_id):
    return get_html(get_contest_rank_url(contest_id))


# Return: problem statement in HTML
def get_problem_statement(soup):
    # Remove problem title
    soup.find("table", {"style": "margin-top:10px"}).decompose()

    # Remove Google +1 button
    soup.find("div", {"style": "position: absolute; right: 0px"}).decompose()

    # Remove Google ads
    soup.find("div", {"class": "aProblemTop"}).decompose()

    # Remove FB like button
    soup.find("div", {"class": "fb-like"}).decompose()

    # Remove problem information (at the bottom)
    soup.find("table", {"class": "probleminfo"}).decompose()

    # Remove users' comment
    soup.find("div", {"id": "ccontent"}).decompose()

    # problem statement
    prob_content = soup.find("div", {"class": "prob"})

    prob_statement = prob_content.prettify()

    prob_statement = prob_statement.replace("../../../SPOJVN", "http://vn.spoj.com/SPOJVN")

    return prob_statement


# Return: author's handle
def get_problem_author(soup):
    table_info = BeautifulSoup(soup.find("table", {"class": "probleminfo"}).prettify())
    author_row = table_info.find_all("tr")[0]
    author_cell = author_row.find_all("td")[1]
    author_url = author_cell.find("a")["href"]
    return author_url[7:]


# Return: problem's crated date as date
def get_problem_created_date(soup):
    table_info = BeautifulSoup(soup.find("table", {"class": "probleminfo"}).prettify())
    date_row = table_info.find_all("tr")[1]
    date_cell = date_row.find_all("td")[1]
    return dateutil.parser.parse(date_cell.text.strip())


# Return: problem's time limit as float (second)
def get_problem_time_limit(soup):
    table_info = BeautifulSoup(soup.find("table", {"class": "probleminfo"}).prettify())
    time_row = table_info.find_all("tr")[2]
    time_cell = time_row.find_all("td")[1]
    time_elements = time_cell.text.split("-")
    return float(time_elements[len(time_elements) - 1].replace("s", ""))


# Return: problem's source limit as int (Byte)
def get_problem_source_limit(soup):
    table_info = BeautifulSoup(soup.find("table", {"class": "probleminfo"}).prettify())
    time_row = table_info.find_all("tr")[3]
    time_cell = time_row.find_all("td")[1]
    return int(time_cell.text.strip().replace("B", ""))


# Return: problem's memory limit as string (parse if needed)
def get_problem_memory_limit(soup):
    table_info = BeautifulSoup(soup.find("table", {"class": "probleminfo"}).prettify())
    mem_row = table_info.find_all("tr")[4]
    mem_cell = mem_row.find_all("td")[1]
    return int(mem_cell.text.strip().replace("MB", ""))


# Return: problem's cluster as string
def get_problem_cluster(soup):
    table_info = BeautifulSoup(soup.find("table", {"class": "probleminfo"}).prettify())
    cluster_row = table_info.find_all("tr")[5]
    cluster_cell = cluster_row.find_all("td")[1]
    return cluster_cell.text.strip()


# Return: problem's source as a string
def get_problem_source(soup):
    table_info = BeautifulSoup(soup.find("table", {"class": "probleminfo"}).prettify())
    if len(table_info.find_all("tr")) < 8:
        return ""
    src_row = table_info.find_all("tr")[7]
    src_cell = src_row.find_all("td")[1]
    return src_cell.text.strip()


# Find available language for a problem
# Return: array of language code
def get_problem_languages(problem_code):
    url = get_problem_submit_url(problem_code)
    soup = get_html(url)
    langs = BeautifulSoup(soup.find("select", {"name": "lang", "id": "lang"}).prettify())
    options = langs.find_all("option")

    languages = []
    for option in options:
        languages.append({"id": option["value"],
                          "name": option.text.strip()})
    return languages


def get_problem(problem_code, problem_id, problem_name, category):
    # Check if problem is exists in database
    problem = SpojProblem.objects.filter(code=problem_code)
    if len(problem) == 0:
        problem = SpojProblem.objects.create(
            code=problem_code,
            problem_id=problem_id,
            name=problem_name,
            category=category
        )
        need_update_statement = True
    else:
        need_update_statement = False
        problem = problem[0]

    # Crawling problem statement
    # need_update_statement = True
    if need_update_statement:
        prob_html = get_problem_html(problem_code)
        problem.author = get_problem_author(prob_html)
        problem.created_at = get_problem_created_date(prob_html)
        problem.time_limit = get_problem_time_limit(prob_html)
        problem.source_limit = get_problem_source_limit(prob_html)
        problem.memory_limit = get_problem_memory_limit(prob_html)
        problem.problem_source = get_problem_source(prob_html)
        problem.statement = get_problem_statement(prob_html)

        languages = get_problem_languages(problem_code)
        for language in languages:
            lang = SpojProblemLanguage.objects.filter(lang_id=int(language["id"]))
            if len(lang) is not 0:
                problem.allowed_languages.add(lang[0])

    problem.save()

    return problem


def get_problem_codes_from_category(category):
    result = []

    print sys.getdefaultencoding()
    print sys.stdin.encoding
    print sys.stdout.encoding

    page_id = 0
    while True:

        # if page_id == 1:
            # return result

        problem_rows = get_elements_from_url(get_category_url(category, page_id=page_id), 'tr[class="problemrow"]')

        if problem_rows is None:
            break

        for problem_row in problem_rows:
            text = problem_row.__str__().replace('\n', ' ')
            matcher = PROBLEM_RE.match(text)

            if matcher:
                data = matcher.groupdict()
                print u'Crawling %s - %s' % (data['code'], data['name'])

                problem = get_problem(problem_code=data['code'], problem_id=data['id'], problem_name=data['name'], category=category)

                if category.name == 'acm':
                    problem.accept_count = data['ac_count']
                    problem.accept_rate = data['ac_rate']
                    problem.score = round(80.0 / (40 + int(data['ac_count'])), 1)
                    problem.save()

                time.sleep(1)

                result.append(problem)

        page_id += 1

    return result


# save all languages and save to database
def save_all_languages():
    url = VOJ_TEST_URL
    soup = get_html(url)
    langs = BeautifulSoup(soup.find("select", {"name": "lang", "id": "lang"}).prettify())
    options = langs.find_all("option")

    for option in options:
        # Check if problem is exists in database
        spojlang = SpojProblemLanguage.objects.filter(lang_id=int(option["value"]))
        if len(spojlang) == 0:
            spojlang = SpojProblemLanguage.objects.create(lang_id=int(option["value"]),
                                                          name=option.text.strip())
        else:
            spojlang = spojlang[0]

        spojlang.name = option.text.strip()
        spojlang.save()
