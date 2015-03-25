from django.shortcuts import render, get_object_or_404
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


def show(request, code):
    problem = get_object_or_404(SpojProblem, code=code)
    return render(request, 'problems/problem_show.html', {
        'problem': problem
    })
