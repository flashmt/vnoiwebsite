# -*- coding: utf-8 -*-
import time
import re
import requests
import html5lib
import dateutil.parser
import copy
import json

from bs4 import BeautifulSoup

from contests.models import ContestStandingTable


VOJ_BASE_URL = 'http://vn.spoj.com/'
# this url is used to get all languages
VOJ_TEST_URL = 'http://vn.spoj.com/submit/TEST/'


def get_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    # Since the problem statement of SPOJ sometimes contains '&', '<' and '>', which are not valid in correct HTML,
    # we must use a lenient parser
    return BeautifulSoup(response.text.replace(u'ð', u'đ'), 'html5lib')


def get_elements_from_html(html, selector):
    if html is None:
        return None
    return html.select(selector)


def get_elements_from_url(url, selector):
    return get_elements_from_html(get_html(url), selector)


def get_contest_rank_url(contest_id):
    return '%s%s/ranks' % (VOJ_BASE_URL, contest_id)


def get_contest_rank_html(contest_id):
    return get_html(get_contest_rank_url(contest_id))


# download a contest standings and save to Database (overwrite the old one)
def crawl_old_voj_contest(contest_id):
    soup = get_contest_rank_html(contest_id)
    soup = BeautifulSoup(soup.find("td", {"class": "content"}).prettify())
    titles = soup.find_all("h4")[1:]
    tables = soup.find_all("table", {"class": "problems"})[1:]

    size = len(titles)

    for i in range(0, size):
        # Ignore empty tables
        if len(titles[i].text.strip()) == 0:
            continue

        print '%s' % (titles[i].text.strip())

        spoj_table = ContestStandingTable.objects.filter(code=contest_id, name=titles[i].text.strip())
        if len(spoj_table) == 0:
            spoj_table = ContestStandingTable.objects.create(code=contest_id, name=titles[i].text.strip())
        else:
            spoj_table = spoj_table[0]

        table_soup = BeautifulSoup(tables[i].prettify())

        title_arr = []
        titles_soup = BeautifulSoup(table_soup.find("tr", {"class": "headerrow"}).prettify())
        titles_soup = titles_soup.find_all("th")
        for title in titles_soup:
            string = title.text.split()
            col_name = ""
            for token in string:
                col_name = col_name + token + " "
            title_arr.append(col_name)
        spoj_table.title = json.dumps(title_arr)

        content_arr = []
        rows = table_soup.find_all("tr", {"class": "problemrow"})
        for row in rows:
            row_arr = []

            row_soup = BeautifulSoup(row.prettify())
            cells = row.find_all("td", {"class": "mini"})

            for cell in cells:
                row_arr.append(cell.text.strip())

            content_arr.append(row_arr)
        spoj_table.content = json.dumps(content_arr)

        spoj_table.save()
