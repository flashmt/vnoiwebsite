import authority
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()
authority.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', include('main.urls', namespace="main")),
    url(r'^forum/', include('forum.urls', namespace="forum")),
    url(r'^user/', include('vnoiusers.urls', namespace="user")),
    url(r'^message/', include('vnoimessages.urls', namespace="message")),
    # url(r'^postman/', include('postman.urls')),
    url(r'^authority/', include('authority.urls')),
    url(r'^problem/', include('problems.urls', namespace='problems')),
)

