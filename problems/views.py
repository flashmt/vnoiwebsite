from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from problems.models import SpojProblem, SpojProblemForum
from forum.models import ForumGroup
from forum.views import topic_list


def index(request):
    problems = SpojProblem.objects.all().values(
        'code',
        'name',
        'category__name',
        'accept_count',
        'score',
    )
    return render(request, 'problems/problem_list.html', {
        'problems': problems
    })


def show(request, code):
    problem = get_object_or_404(SpojProblem, code=code)
    return render(request, 'problems/problem_show.html', {
        'problem': problem
    })


def discuss(request, code):
    problem = get_object_or_404(SpojProblem, code=code)
    problem_forum_group = ForumGroup.objects.get(group_type='p')
    forum, created = SpojProblemForum.objects.get_or_create(
        problem=problem,
        created_by=request.user,
        forum_group=problem_forum_group,
        name=code + ' - Discuss'
    )
    return topic_list(
        request,
        forum_id=forum.id,
        template='problems/problem_discuss.html',
        extra_context={'problem': problem}
    )
