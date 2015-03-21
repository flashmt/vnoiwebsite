from django.shortcuts import render
from forum.models import ForumGroup


def index(request):
    return render(request, 'vnoilib/index.html', {
        'lib_groups': ForumGroup.objects.filter(name__startswith='Library')
    })