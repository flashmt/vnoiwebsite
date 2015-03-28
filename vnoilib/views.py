from django.shortcuts import render, get_object_or_404
from forum.models import ForumGroup, Forum, Topic
from forum.views import pagination_items


def index(request):
    return render(request, 'vnoilib/index.html', {
        'lib_groups': ForumGroup.objects.filter(group_type='l')
    })


def topic_retrieve(request, forum_id, topic_id, template="vnoilib/post_view.html"):
    forum = get_object_or_404(Forum, pk=forum_id)
    topic = get_object_or_404(Topic, pk=topic_id)
    posts = topic.posts.all().values('content', 'created_at', 'created_by__id', 'created_by')
    return render(request, template, {
        'forum': forum,
        'topic': topic,
        'post': topic.post,
        'posts': posts
    })


def topic_list(request, forum_id, template="vnoilib/topic_list.html"):
    forum = get_object_or_404(Forum, pk=forum_id)
    topics = Topic.objects.filter(forum_id=forum_id)
    topics = pagination_items(request, topics, 50)
    return render(request, template, {
        'forum': forum,
        'topics': topics,
        'lib_groups': ForumGroup.objects.filter(group_type='l')
    })
