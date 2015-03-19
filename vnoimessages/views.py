from __future__ import unicode_literals
from django.http import HttpResponse


def index(request):
    return HttpResponse("This is message home")


def inbox(request):
    return HttpResponse("This is inbox page")
