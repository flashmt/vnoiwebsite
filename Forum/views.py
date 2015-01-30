from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from forum.models import Topic


def index(request):
    topics = Topic.objects.all()
    return render(request, 'forum/forum_index.html', {'topics': topics})

def list(request):
    return HttpResponse("this is list!")
