import authority
from django.conf.urls import patterns, include, url
from django.contrib import admin

# TODO: When upgrade to 1.8, re-enable this
import warnings
from django.utils.deprecation import RemovedInDjango18Warning
from configurations import settings

warnings.filterwarnings("ignore", category=RemovedInDjango18Warning)

admin.autodiscover()
authority.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('main.urls', namespace="main")),
    url(r'^forum/', include('forum.urls', namespace="forum")),
    url(r'^user/', include('vnoiusers.urls', namespace="user")),
    url(r'^message/', include('vnoimessages.urls', namespace="message")),
    # url(r'^postman/', include('postman.urls')),
    url(r'^authority/', include('authority.urls')),
    url(r'^problems/', include('problems.urls', namespace='problems')),
    url(r'^contests/', include('contests.urls', namespace='contests')),
    url(r'^library/', include('vnoilib.urls', namespace='library')),
    # url(r'^avatar/', include('avatar.urls')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))
