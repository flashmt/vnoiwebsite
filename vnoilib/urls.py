from django.conf.urls import patterns, url
from vnoilib import views
from forum import views as forum_views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<forum_id>\d+)/(?P<topic_id>\d+)/$', forum_views.topic_retrieve, name="topic_retrieve"),
    url(r'^(?P<forum_id>\d+)/$', views.topic_list, name="topic_list"),
)
