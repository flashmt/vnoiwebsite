from __future__ import unicode_literals

from django.conf.urls import patterns, url
import postman
from vnoimessages import views
from django.views.generic.base import RedirectView

from postman import OPTIONS
from postman.views import (InboxView, SentView, ArchivesView, TrashView,
                           WriteView, ReplyView, MessageView, ConversationView,
                           ArchiveView, DeleteView, UndeleteView)


urlpatterns = patterns(
    '',
    url(r'^$',  RedirectView.as_view(url='inbox/'), name='index'),
    url(r'^inbox/(?:(?P<option>'+OPTIONS+')/)?$', InboxView.as_view(template_name="vnoimessages/inbox.html"), name='inbox'),
    url(r'^sent/(?:(?P<option>'+OPTIONS+')/)?$', SentView.as_view(template_name="vnoimessages/sent.html"), name='sent'),
    url(r'^archives/(?:(?P<option>'+OPTIONS+')/)?$', ArchivesView.as_view(template_name="vnoimessages/archives.html"), name='archives'),
    url(r'^trash/(?:(?P<option>'+OPTIONS+')/)?$', TrashView.as_view(template_name='vnoimessages/trash.html'), name='trash'),
    url(r'^write/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(template_name='vnoimessages/write.html'), name='write'),
    url(r'^reply/(?P<message_id>[\d]+)/$', ReplyView.as_view(template_name='vnoimessages/reply.html'), name='reply'),
    url(r'^view/(?P<message_id>[\d]+)/$', MessageView.as_view(template_name='vnoimessages/view.html'), name='view'),
    url(r'^view/t/(?P<thread_id>[\d]+)/$', ConversationView.as_view(template_name="vnoimessages/view.html"), name='view_conversation'),
    url(r'^archive/$', ArchiveView.as_view(), name='archive'),
    url(r'^delete/$', DeleteView.as_view(), name='delete'),
    url(r'^undelete/$', UndeleteView.as_view(), name='undelete'),
    (r'^$', RedirectView.as_view(url='inbox/')),

)

