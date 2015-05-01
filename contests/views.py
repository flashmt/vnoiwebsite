from django.shortcuts import render, get_object_or_404
from contests.models import ContestStandingTable
import json

# Create your views here.


def index(request):
    contests = ContestStandingTable.objects.all()
    return render(request, 'contests/contest_list.html', {
        'contests': contests,
        'disable_breadcrumbs': True
        })


def show_table(request, contest_id):
    contest = get_object_or_404(ContestStandingTable, id=contest_id)
    return render(request, 'contests/contest_show.html', {
        'contest': contest.code + ' - ' + contest.name,
        'contest_title': json.loads(contest.title),
        'contest_table': json.loads(contest.content),
        'disable_breadcrumbs': True
        })
    pass
