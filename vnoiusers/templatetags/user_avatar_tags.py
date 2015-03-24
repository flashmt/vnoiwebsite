import hashlib
from django import template
from vnoiusers.user_avatar_util import thumbnail_exists, avatar_url

try:
    from urllib.parse import urljoin, urlencode
except ImportError:
    from urlparse import urljoin
    from urllib import urlencode

from avatar.util import get_default_avatar_url
from django.utils.encoding import force_bytes
from avatar.conf import settings

register = template.Library()


@register.simple_tag
def user_avatar_url(user, size=settings.AVATAR_DEFAULT_SIZE):
    """
        This method is reimplemented avatar_url in avatar.templatetags
        in order to optimize query db number for avatar.
    """
    avatar = user.profile.avatar
    if avatar:
        if not thumbnail_exists(user, avatar, size):
            avatar.create_thumbnail(size)
        return avatar_url(user, avatar, size)

    if settings.AVATAR_GRAVATAR_BACKUP:
        params = {'s': str(size)}
        if settings.AVATAR_GRAVATAR_DEFAULT:
            params['d'] = settings.AVATAR_GRAVATAR_DEFAULT
        path = "%s/?%s" % (hashlib.md5(force_bytes(user.email)).hexdigest(),
                           urlencode(params))
        return urljoin(settings.AVATAR_GRAVATAR_BASE_URL, path)

    return get_default_avatar_url()


