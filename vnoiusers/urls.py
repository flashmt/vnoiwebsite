from django.conf.urls import patterns, url
from vnoiusers import views

urlpatterns = patterns(
    '',
    url(r'^login$', views.user_login, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),
    url(r'^register$', views.user_create, name='register'),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm, name='register_confirm'),
    url(r'^update_profile$', views.update_profile, name='update_profile'),
    url(r'^(?P<user_id>\d+)/$', views.user_profile, name='profile'),
    url(r'^upload_avatar$', views.user_upload_avatar, name='upload_avatar'),
    url(r'^link_codeforces$', views.link_codeforces_account, name='link_codeforces'),
    url(r'^unlink_codeforces$', views.unlink_codeforces_account, name='unlink_codeforces'),
    url(r'^link_voj$', views.link_voj_account, name='link_voj'),
    url(r'^unlink_voj$', views.unlink_voj_account, name='unlink_voj'),
    url(r'^add_friend/(?P<user_id>\d+)$', views.add_friend, name='add_friend'),
    url(r'^remove_friend/(?P<user_id>\d+)$', views.remove_friend, name='remove_friend'),
    url(r'^friend_list$', views.friend_list, name='friend_list'),
    url(r'^index$', views.index, name='index'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    url(r'^password_change/done/$', views.password_change_done, name='password_change_done'),
    url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/complete/$', views.password_reset_complete, name='password_reset_complete'),
)


