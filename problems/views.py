from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from problems.models import SpojProblem, SpojProblemForum
from forum.models import ForumGroup
from forum.views import topic_list
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    problem_list = SpojProblem.objects.all().values(
        'code',
        'name',
        'category__name',
        'accept_count',
        'score',
    )
    paginator = Paginator(problem_list, 50)

    page = request.GET.get('page')
    try:
        problems = paginator.page(page)
    except PageNotAnInteger:
        problems = paginator.page(1)
    except EmptyPage:
        problems = paginator.page(paginator.num_pages)

    start = max(min(paginator.num_pages - 10, problems.number - 5), 1)

    return render(request, 'problems/problem_list.html', {
        'problems': problems,
        'page_range': range(start, start + 11),
        'disable_breadcrumbs': True
    })


def show(request, code):
    problem = get_object_or_404(SpojProblem, code=code)
    return render(request, 'problems/problem_show.html', {
        'problem': problem
    })


@login_required
def discuss(request, code):
    problem = get_object_or_404(SpojProblem, code=code)
    problem_forum_group = ForumGroup.objects.get(group_type='p')

    # Create new forum for this problem, or retrieve the one that already exists
    # Note:
    # - Since created_by can not be None, we must specify some value.
    #   But, if we use request.user, then get_or_create will not find existing
    #   forum created by different user. So the most easy way is to set it to
    #   2nd user (vnoiuser)
    forum, created = SpojProblemForum.objects.get_or_create(
        problem=problem,
        forum_group=problem_forum_group,
        created_by=User.objects.get(pk=2),
        # Name must be equal to code - see models.py for more details
        name=code
    )
    return topic_list(
        request,
        forum_id=forum.id,
        template='problems/problem_discuss.html',
        extra_context={'problem': problem}
    )


@login_required
def submit(request, code):
    problem = get_object_or_404(SpojProblem, code=code)
    return render(request, 'problems/problem_submit.html', {
        'problem': problem
    })


def status(request, code):
    problem = get_object_or_404(SpojProblem, code=code)
    return render(request, 'problems/problem_status.html', {
        'problem': problem
    })


def rank(request, code):
    problem = get_object_or_404(SpojProblem, code=code)
    return render(request, 'problems/problem_rank.html', {
        'problem': problem
    })
