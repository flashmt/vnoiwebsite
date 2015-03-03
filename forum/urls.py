from django.conf.urls import patterns, url
from forum import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<forum_id>\d+)/topic_create/$', views.topic_create, name='topic_create'),
    url(r'^(?P<forum_id>\d+)/(?P<topic_id>\d+)/$', views.topic_retrieve, name="topic_retrieve"),
    url(r'^(?P<forum_id>\d+)/(?P<topic_id>\d+)/(?P<post_id>\d+)/post_create/$', views.post_create, name="post_create"),
    url(r'^(?P<forum_id>\d+)/(?P<topic_id>\d+)/(?P<post_id>\d+)/post_update/$', views.post_update, name="post_update"),
    url(r'^(?P<forum_id>\d+)/$', views.topic_list, name="topic_list"),
    url(r'^vote/(?P<post_id>\d+)/$', views.vote_create, name="vote_create"),
)
