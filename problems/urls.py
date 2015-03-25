from django.conf.urls import patterns, url
from problems import views

urlpatterns = patterns(
    '',
    url(r'^list$', views.index, name='list'),
    url(r'^show/(?P<code>[\w]{2,12})/$', views.show, name='show'),
)
