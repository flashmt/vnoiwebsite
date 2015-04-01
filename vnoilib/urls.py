from django.conf.urls import patterns, url
from vnoilib import views
from forum import views as forum_views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<forum_id>\d+)/(?P<topic_id>\d+)/$', forum_views.topic_retrieve, name="topic_retrieve",
        kwargs={'template': 'vnoilib/post_view.html'}),
    url(r'^(?P<forum_id>\d+)/$', views.topic_list, name="topic_list"),
    url(r'^(?P<forum_id>\d+)/topic_create/$', views.topic_create, name='topic_create'),
)
