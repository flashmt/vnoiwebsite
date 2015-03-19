from django.shortcuts import render
from forum.models import PinnedTopic, Post

# Create your views here.


def index(request):
    pinned_topics = []
    for topic in PinnedTopic.objects.all():
        pinned_topics.append({
            'title': topic.post.title,
            'forum_id': topic.post.topic.forum_id,
            'topic_id': topic.post.topic_id,
            'author': topic.post.created_by,
            'content': topic.post.content,
            'total_vote': topic.post.total_votes(),
            'post_id': topic.post_id,
        })
    recent_posts = []
    posts = Post.objects.order_by('-created_at').values(
        'pk', 'created_by__username', 'topic__title', 'topic__id', 'topic__forum__id')[:5]
    for post in posts:
        recent_posts.append({
            'post_id': post['pk'],
            'author': post['created_by__username'],
            'topic_title': post['topic__title'],
            'topic_id': post['topic__id'],
            'forum_id': post['topic__forum__id'],
        })
    return render(request, 'main/home.html', {
        'pinned_topics': pinned_topics,
        'recent_posts': recent_posts,
    })
