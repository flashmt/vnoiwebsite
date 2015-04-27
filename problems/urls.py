from django.conf.urls import patterns, url
from problems import views

urlpatterns = patterns(
    '',
    url(r'^list/$', views.index, name='list'),
    url(r'^show/(?P<code>[\w]{2,12})/$', views.show, name='show'),
    url(r'^discuss/(?P<code>[\w]{2,12})/$', views.discuss, name='discuss'),
    url(r'^submit/(?P<code>[\w]{2,12})/$', views.submit, name='submit'),
    url(r'^status/(?P<code>[\w]{2,12})/$', views.status, name='status'),
    url(r'^rank/(?P<code>[\w]{2,12})/$', views.rank, name='rank'),
)
