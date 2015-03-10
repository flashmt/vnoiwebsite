from django.shortcuts import render
from forum.models import PinnedTopic

# Create your views here.


def index(request):
    pinned_posts = PinnedTopic.objects.all()
    return render(request, 'main/home.html', {
        'pinned_posts': pinned_posts
    })
