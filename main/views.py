from django.shortcuts import render
from forum.models import PinnedTopic

# Create your views here.


def index(request):
    pinned_posts = PinnedTopic.objects.all()
    results = []
    for topic in pinned_posts:
        print topic.post.created_by
        results.append({
            'title': topic.post.title,
            'forum_id': topic.post.topic.forum_id,
            'topic_id': topic.post.topic_id,
            'author': topic.post.created_by,
            'content': topic.post.content,
            'total_vote': topic.post.total_votes(),
            'post_id': topic.post_id,
        })
    return render(request, 'main/home.html', {
        'pinned_topics': results
    })
