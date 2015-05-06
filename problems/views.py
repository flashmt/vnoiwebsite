from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from problems.forms import VojSubmitForm
from problems.models import SpojProblem, SpojProblemForum, SpojProblemSubmission
from forum.models import ForumGroup
from forum.views import topic_list
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from voj_interface.submit import voj_submit


def index(request):
    problem_list = SpojProblem.objects.all().order_by('created_at').values(
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

    # TODO: If user haven't linked VOJ account --> redirect to link VOJ account page

    template_name = 'problems/problem_submit.html'
    if request.POST:
        form = VojSubmitForm(request.POST)
        if form.is_valid():
            # TODO
            # At this point, the submitted request is valid (code is not empty, language is valid
            # and also the judge queue is not too long and user haven't submitted too many)

            # Store to DB. Note that at this point, we do not yet have the submission ID.
            # Later, the status crawler will discover this submission and then, will update
            # this submission ID, and hopefully, will also update the status
            SpojProblemSubmission.objects.create(
                problem=problem,
                # voj_account=request.user.profile.voj_account
                # submission_language=form.cleaned_data['language'] <-- or something like that
                # submission_time=now
                # submission_id and submission_verdict will be crawled later
            )

            # Submit the code to VOJ
            voj_submit(request.user, form.cleaned_data['code'], form.cleaned_data['language'])

            # Then, just redirect user to status page of problem
            return HttpResponseRedirect(reverse('problems:status', kwargs={'code': problem.code}))
        else:
            return render(request, template_name, {
                'form': form,
                'message': form.errors
            })
    else:
        return render(request, template_name, {
            'problem': problem,
            'form': VojSubmitForm
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
