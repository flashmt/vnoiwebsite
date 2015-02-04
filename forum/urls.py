from django.conf.urls import patterns, url
from forum import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^list/$', views.list, name='list'),
    url(r'^(?P<forum_id>\d+)/post_create/$', views.post_create, name='post_create'),
    url(r'^post_update/(?P<post_id>\d+)/$', views.post_update, name='post_update'),
    url(r'^(?P<forum_id>\d+)/$', views.topic_list, name="topic_list"),
    url(r'^(?P<forum_id>\d+)/(?P<topic_id>\d+)$', views.topic_retrieve, name="topic_retrieve"),
)
