from django.conf.urls import patterns, url
from contests import views

urlpatterns = patterns(
    '',
    url(r'^list/$', views.index, name='list'),
    url(r'^list/(?P<contest_id>\d+)/$', views.index, name='list'),
    url(r'^show/(?P<contest_id>\d+)/$', views.show_standings, name='standings'),
)
