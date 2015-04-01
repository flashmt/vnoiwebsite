from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from forum.models import ForumGroup, Forum, Topic
from forum.views import pagination_items
from forum import views as forum_views


def index(request):
    lib_group = ForumGroup.objects.filter(group_type='l').first()
    forum = lib_group.forums.first()
    return redirect(reverse('library:topic_list', kwargs={'forum_id': forum.id}))


def topic_list(request, forum_id, template="vnoilib/topic_list.html"):
    forum = get_object_or_404(Forum, pk=forum_id)
    topics = Topic.objects.filter(forum_id=forum_id).select_related(
        'forum__forum_group', 'created_by')
    topics = pagination_items(request, topics, 50)
    return render(request, template, {
        'forum': forum,
        'topics': topics,
        'lib_groups': ForumGroup.objects.filter(group_type='l')
    })


@login_required
def topic_create(request, forum_id=None, template="vnoilib/topic_create.html"):
    return forum_views.topic_create(request, forum_id, template)
