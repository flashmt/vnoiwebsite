import hashlib
import os
from avatar.conf import settings
from avatar.models import find_extension, avatar_storage
from django.utils.encoding import force_bytes


def avatar_file_path(instance=None, user=None, filename=None, size=None, ext=None):
    tmppath = [settings.AVATAR_STORAGE_DIR]
    if settings.AVATAR_HASH_USERDIRNAMES:
        tmp = hashlib.md5(user.username).hexdigest()
        tmppath.extend([tmp[0], tmp[1], user.username])
    else:
        tmppath.append(user.username)
    if not filename:
        # Filename already stored in database
        filename = instance.avatar.name
        if ext and settings.AVATAR_HASH_FILENAMES:
            # An extension was provided, probably because the thumbnail
            # is in a different format than the file. Use it. Because it's
            # only enabled if AVATAR_HASH_FILENAMES is true, we can trust
            # it won't conflict with another filename
            (root, oldext) = os.path.splitext(filename)
            filename = root + "." + ext
    else:
        # File doesn't exist yet
        if settings.AVATAR_HASH_FILENAMES:
            (root, ext) = os.path.splitext(filename)
            filename = hashlib.md5(force_bytes(filename)).hexdigest()
            filename = filename + ext
    if size:
        tmppath.extend(['resized', str(size)])
    tmppath.append(os.path.basename(filename))
    return os.path.join(*tmppath)


def avatar_name(user, avatar, size):
    ext = find_extension(settings.AVATAR_THUMB_FORMAT)
    return avatar_file_path(
        instance=avatar,
        size=size,
        ext=ext,
        user=user,
    )


def thumbnail_exists(user, avatar, size):
    return avatar_storage.exists(avatar_name(user, avatar, size))


def avatar_url(user, avatar, size):
    return avatar_storage.url(avatar_name(user, avatar, size))
