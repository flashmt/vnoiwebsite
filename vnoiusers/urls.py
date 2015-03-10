from django.conf.urls import patterns, url
from vnoiusers import views

urlpatterns = patterns(
    '',
    url(r'^login$', views.user_login, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),
    url(r'^(?P<user_id>\d+)/$', views.user_profile, name = 'user_profile'),
)
