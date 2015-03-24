from django.core.cache import cache
from django.shortcuts import render
from django.utils import timezone
from configurations.cache_keys import *
from externaljudges.models import ContestSchedule
from forum.models import Post, Topic

# Create your views here.
from vnoiusers.models import VnoiUser


def index(request):
    pinned_topics = cache.get(HOME_PINNED_TOPICS)
    if pinned_topics is None:
        pinned_topics = Topic.objects.filter(is_pinned=True)
        cache.set(HOME_PINNED_TOPICS, pinned_topics, HOME_PINNED_TOPICS_CACHE_TIME)

    posts = Post.objects.order_by('-created_at').values(
        'pk', 'created_by__username', 'topic__title', 'topic__id', 'topic__forum__id')[:5]

    return render(request, 'main/home.html', {
        'pinned_topics': pinned_topics,
        'recent_posts': posts,
        'coming_contests': ContestSchedule.objects.filter(start_time__gt=timezone.now()).order_by('start_time'),
        'contributors': VnoiUser.objects.all().order_by('-contribution').values('user__username', 'contribution')[:10]
    })
