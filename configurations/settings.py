"""
Django settings for vnoiwebsite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'iev8%%$ck&vpx&07+fvm%1#aj&1iuumnj&s6r8y3%1%90-+0cz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'forum',
    'main',
    'vnoiusers',
    'bootstrap3',
    'postman',
    'vnoimessages',
    'authority',
    'problems',
    'debug_toolbar',
    'avatar',
    'django_bleach',
    'externaljudges',
    'vnoilib',
    'post_office',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
)

ROOT_URLCONF = 'configurations.urls'

WSGI_APPLICATION = 'configurations.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if 'test' in sys.argv:
    # We use sqlite database for testing, because it is much faster to create
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    # But stick to mysql database for production, because it is more trusted
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'vnoi',
            'USER': 'root',
            'PASSWORD': 'VeryStrongPassword!',
            'HOST': '127.0.0.1',  # Using direct IP instead of localhost, to ensure MySQLdb doesn't fail
            'OPTIONS': {'init_command': 'SET storage_engine=INNODB'}
        },
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'main', 'static')

LOGIN_URL = '/user/login'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'configurations.log',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'forum': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        # TODO: The following is to disable RemovedInDjango18Warning --> when updated to 1.8, need to remove
        'py.warnings': {
            'propagate': False,
            'handlers': [],
        },
        # 'py.warnings': {
        #     'handlers': ['console'],
        # },
    }
}

# To use logger, instantiate logger:
# import logging
# logger = logging.getLogger(__name__)


BOOTSTRAP3 = {
    'horizontal_field_class': 'col-md-6',
}


# Postman settings
POSTMAN_DISALLOW_ANONYMOUS = True
POSTMAN_AUTO_MODERATE_AS = True
POSTMAN_MAILER_APP = None

# Django-authority
AUTHORITY_USE_SMART_CACHE = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Django-avatar setting
AVATAR_MAX_AVATARS_PER_USER = 1

BLEACH_ALLOWED_TAGS = ['p', 'strong', 'em', 'pre', 'code', 'a', 'img', 'ol', 'ul', 'li', 'span', 'br']
BLEACH_ALLOWED_ATTRIBUTES = ['href', 'class', 'alt', 'style', 'src']
BLEACH_STRIP_TAGS = True
BLEACH_STRIP_COMMENTS = True

# ABSOLUTE_URL_OVERRIDES now works on models that don't declare get_absolute_url().
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda user: "/user/%d/" % user.id,
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Email settings
# using post office as the default email backend
EMAIL_BACKEND = 'post_office.EmailBackend'

POST_OFFICE = {
    'DEFAULT_PRIORITY': 'now'
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'vnoiwebsite@gmail.com'
EMAIL_HOST_PASSWORD = 'vnoipassword'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
