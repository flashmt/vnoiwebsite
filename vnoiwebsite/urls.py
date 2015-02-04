from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', include('main.urls', namespace="main")),
    url(r'^forum/', include('forum.urls', namespace="forum")),
    url(r'^user/', include('vnoiusers.urls', namespace="user")),
)
