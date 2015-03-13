from problems.crawler.crawlers import get_problems_from_category
from problems.crawler.models import ProblemCategory

problem_category_acm = ProblemCategory('acm')
problem_category_oi = ProblemCategory('oi')

problems_acm = get_problems_from_category(problem_category_acm)
problems_oi = get_problems_from_category(problem_category_oi)


def array_to_json(arr):
    return '[' + ', '.join([x.to_json() for x in arr]) + ']'

print array_to_json([problem_category_acm, problem_category_oi])
print array_to_json(problems_acm)
print array_to_json(problems_oi)