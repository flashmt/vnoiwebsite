import os

# Before importing some Django lib, we must have this
from django.core.wsgi import get_wsgi_application

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configurations.settings")

from contests.voj.crawlers import crawl_old_voj_contest

if __name__ == "__main__":
    application = get_wsgi_application()
    crawl_old_voj_contest('VO12')
