import os

# Before importing some Django lib, we must have this
from django.core.wsgi import get_wsgi_application

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configurations.settings")

from problems.crawler.crawlers import get_problem_codes_from_category
from problems.models import SpojProblemCategory


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

    problems_acm = get_problem_codes_from_category(problem_category_acm)
    problems_oi = get_problem_codes_from_category(problem_category_oi)

    print [problem_category_acm, problem_category_oi]
