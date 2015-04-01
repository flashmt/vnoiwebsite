from django.core.cache import cache
from django.shortcuts import render
from django.utils import timezone
from configurations.cache_keys import *
from externaljudges.models import ContestSchedule
from forum.models import Post, Topic, Vote

# Create your views here.
from vnoiusers.models import VnoiUser


def index(request):
    pinned_topics = cache.get(HOME_PINNED_TOPICS)
    if pinned_topics is None:
        pinned_topics = Topic.objects.filter(is_pinned=True).values(
            'id', 'forum', 'title', 'content',
            'created_by', 'created_by__username', 'created_at',
            'post__id', 'post__num_upvotes', 'post__num_downvotes',
            'forum__forum_group__group_type'
        )
        cache.set(HOME_PINNED_TOPICS, pinned_topics, HOME_PINNED_TOPICS_CACHE_TIME)

    # Since sqlite does not support select distinct, we must make it distinct by flatten QuerySet and then
    #  wrapping it in a set
    recent_posts = set(Post.objects.values_list(
        'created_by__username', 'topic__title', 'topic__id', 'topic__forum__id'
    ).order_by('-created_at')[:20])
    # and then convert the set to nicely looking array of hash
    posts = []
    for post in recent_posts:
        posts.append({
            'created_by__username': post[0],
            'topic__title': post[1],
            'topic__id': post[2],
            'topic__forum__id': post[3]
        })

    if request.user.is_authenticated():
        post_ids = Post.objects.filter(topic__is_pinned=True).values('id')
        votes = Vote.objects.filter(post_id__in=post_ids, created_by=request.user).values('post_id', 'type')
    else:
        votes = None

    coming_contests = cache.get(HOME_COMING_CONTESTS)
    if coming_contests is None:
        coming_contests = ContestSchedule.objects.filter(start_time__gt=timezone.now()).order_by('start_time')
        cache.set(HOME_COMING_CONTESTS, coming_contests, HOME_COMING_CONTESTS_CACHE_TIME)

    contributors = cache.get(HOME_CONTRIBUTORS)
    if contributors is None:
        contributors = VnoiUser.objects.all().order_by('-contribution').values('user__username', 'contribution')[:10]
        cache.set(HOME_CONTRIBUTORS, contributors, HOME_CONTRIBUTORS_CACHE_TIME)

    return render(request, 'main/home.html', {
        'pinned_topics': pinned_topics,
        'recent_posts': posts,
        'coming_contests': coming_contests,
        'contributors': contributors,
        'votes': votes
    })
