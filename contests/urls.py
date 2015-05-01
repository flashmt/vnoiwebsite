from django.conf.urls import patterns, url
from contests import views

urlpatterns = patterns(
    '',
    url(r'^list/$', views.index, name='list'),
    url(r'^show/(?P<contest_id>\d+)/$', views.show_table, name='show_table'),
)
