from django.shortcuts import render
from problems.models import SpojProblem


def index(request):
    problems = SpojProblem.objects.all().values(
        'code',
        'name',
        'category__name',
        'accept_count',
        'score',
    )
    return render(request, 'problems/problem_list.html', {'problems': problems})