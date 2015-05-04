# To run: python -m contests.voj.main

import os
import sys
import codecs

# Before importing some Django lib, we must have this
from django.core.wsgi import get_wsgi_application

if __name__ == "__main__":
    # Change python encoding
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
    sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
    sys.stderr = codecs.getwriter('UTF-8')(sys.stderr)
    # Import Django environment
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configurations.settings")

from contests.voj.crawlers import crawl_old_voj_contest

if __name__ == "__main__":
    application = get_wsgi_application()
    crawl_old_voj_contest('VO12', 'Vnoi Online 2012', True)
    crawl_old_voj_contest('VM12', 'Vnoi Marathon 2012', True)
    crawl_old_voj_contest('VO13', 'Vnoi Online 2013', True)
    crawl_old_voj_contest('VM13', 'Vnoi Marathon 2013', True)
    crawl_old_voj_contest('VO14', 'Vnoi Online 2014', True)
    crawl_old_voj_contest('VM14', 'Vnoi Marathon 2014', True)
    crawl_old_voj_contest('VO15', 'Vnoi Online 2015', True)
