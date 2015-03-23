import hashlib
from django import template

try:
    from urllib.parse import urljoin, urlencode
except ImportError:
    from urlparse import urljoin
    from urllib import urlencode

from avatar.models import avatar_storage
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
    if user.avatar_name:
        return avatar_storage.url(user.avatar_name(size))

    if settings.AVATAR_GRAVATAR_BACKUP:
        params = {'s': str(size)}
        if settings.AVATAR_GRAVATAR_DEFAULT:
            params['d'] = settings.AVATAR_GRAVATAR_DEFAULT
        path = "%s/?%s" % (hashlib.md5(force_bytes(user.email)).hexdigest(),
                           urlencode(params))
        return urljoin(settings.AVATAR_GRAVATAR_BASE_URL, path)

    # return default avatar url
    return get_default_avatar_url()


