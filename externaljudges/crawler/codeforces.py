# -*- coding: utf-8 -*-

import requests
import os

from bs4 import BeautifulSoup
from datetime import timedelta
from django.utils import timezone
from django.core.wsgi import get_wsgi_application


def cf_contest_list_crawl():
    url = 'http://codeforces.com/api/contest.list?gym=false'
    print 'Retrieving CF contest from %s' % url
    response = requests.get(url).json()

    if response['status'] != 'OK':
        print 'Something bad happened. Cannot crawl :('
    else:
        for contest in response['result']:
            contest_name = contest['name'].encode('utf-8')
            if contest['phase'] == 'BEFORE':
                contests = ContestSchedule.objects.filter(contest_name=contest_name)
                if not contests or len(contests) == 0:
                    contest = ContestSchedule(
                        judge='cf',
                        contest_name=contest_name,
                        start_time=timezone.now() + timedelta(seconds=-contest['relativeTimeSeconds']),
                        duration=contest['durationSeconds']/60,
                        url='http://codeforces.com/contests'
                    )
                    contest.save()


def verify_codeforces_account(username, password):
    url = 'http://codeforces.com/enter'
    data = {
        'csrf_token': '9042909a39d809c14acb4d720889c698',
        'handle': username,
        'password': password,
        'action': 'enter',
        '_tta': '182',
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        return {
            'success': False,
            'message': 'Không kết nối được với server Codeforces. Xin vui lòng thử lại sau',
        }
    else:
        header_text = BeautifulSoup(response.text).find(id='header').text
        if username in header_text:
            return {
                'success': True,
                'message': '',
            }
        else:
            return {
                'success': False,
                'message': 'Tài khoản hoặc mật khẩu không đúng',
            }


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configurations.settings")
    from externaljudges.models import ContestSchedule
    application = get_wsgi_application()
    cf_contest_list_crawl()
