from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from forum.models import PinnedTopic, Post

# Create your views here.


def index(request):
    pinned_topics = PinnedTopic.objects.all()
    for pinned_topic in pinned_topics:
        if not pinned_topic.is_cached:
            post = pinned_topic.post

            pinned_topic.is_cached = True
            pinned_topic.topic_title = post.topic.title
            pinned_topic.forum_id = post.topic.forum_id
            pinned_topic.topic_id = post.topic_id
            pinned_topic.author = post.created_by.username
            pinned_topic.content = post.content
            pinned_topic.last_updated = timezone.now()
            pinned_topic.total_vote = pinned_topic.post.total_votes()
            pinned_topic.save()

        if pinned_topic.last_updated < timezone.now() - timedelta(minutes=30):
            pinned_topic.total_vote = pinned_topic.post.total_votes()
            pinned_topic.last_updated = timezone.now()
            pinned_topic.save()

    posts = Post.objects.order_by('-created_at').values(
        'pk', 'created_by__username', 'topic__title', 'topic__id', 'topic__forum__id')[:5]
    return render(request, 'main/home.html', {
        'pinned_topics': PinnedTopic.objects.all(),
        'recent_posts': posts,
    })
