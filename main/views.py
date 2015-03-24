from django.shortcuts import render
from django.utils import timezone
from externaljudges.models import ContestSchedule
from forum.models import PinnedTopic, Post

# Create your views here.
from vnoiusers.models import VnoiUser


def index(request):
    pinned_topics = PinnedTopic.objects.all().select_related('topic')

    posts = Post.objects.order_by('-created_at').values(
        'pk', 'created_by__username', 'topic__title', 'topic__id', 'topic__forum__id')[:5]

    return render(request, 'main/home.html', {
        'pinned_topics': pinned_topics,
        'recent_posts': posts,
        'coming_contests': ContestSchedule.objects.filter(start_time__gt=timezone.now()).order_by('start_time'),
        'contributors': VnoiUser.objects.all().order_by('-contribution').values('user__username', 'contribution')[:10]
    })
