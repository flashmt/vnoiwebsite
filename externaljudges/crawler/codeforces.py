import requests
import os

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


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configurations.settings")
    from externaljudges.models import ContestSchedule
    application = get_wsgi_application()
    cf_contest_list_crawl()
