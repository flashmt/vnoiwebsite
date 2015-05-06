from django.shortcuts import render, get_object_or_404
from contests.models import *
import json

# Create your views here.


def index(request, contest_id=None):
    contest_groups = ContestGroup.objects.all().select_related('Contest', 'ContestStanding')
    if contest_id is None:
        contest_id = contest_groups.first().contests.first().id
    else:
        contest_id = int(contest_id)

    contest = Contest.objects.get(pk=contest_id)
    return render(request, 'contests/contest_list.html', {
        'contest_groups': contest_groups,
        'contest_id': contest_id,
        'contest': contest,
        'resources': contest.resources,
        'standings': contest.standings,
        'disable_breadcrumbs': True
    })


def show_standings(request, contest_id):
    standing = get_object_or_404(ContestStanding, id=contest_id)
    return render(request, 'contests/contest_show.html', {
        'contest': standing,
        'contest_title': json.loads(standing.title),
        'contest_table': json.loads(standing.content),
    })
