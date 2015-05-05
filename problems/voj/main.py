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

from problems.voj.crawlers import get_problem_codes_from_category
from problems.voj.crawlers import save_all_languages
from problems.voj.crawlers import get_all_accepted_submissions
from problems.models import SpojProblemCategory
from problems.models import SpojProblem

if __name__ == "__main__":

    application = get_wsgi_application()

    problem_category_acm = SpojProblemCategory.objects.filter(name='acm')
    if len(problem_category_acm) == 0:
        problem_category_acm = SpojProblemCategory.objects.create(name='acm')
        problem_category_acm.save()
    else:
        problem_category_acm = problem_category_acm[0]

    problem_category_oi = SpojProblemCategory.objects.filter(name='oi')
    if len(problem_category_oi) == 0:
        problem_category_oi = SpojProblemCategory.objects.create(name='oi')
        problem_category_oi.save()
    else:
        problem_category_oi = problem_category_oi[0]

    save_all_languages()
    for problem in SpojProblem.objects.all():
        get_all_accepted_submissions(problem_code=problem.code, force_crawl=True)

    # problems_acm = get_problem_codes_from_category(problem_category_acm)
    # problems_oi = get_problem_codes_from_category(problem_category_oi)

    # print [problem_category_acm, problem_category_oi]
