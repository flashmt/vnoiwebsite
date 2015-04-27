# -*- coding: utf-8 -*-

from django.core.urlresolvers import resolve, reverse

from django.test import TestCase
from django.test import Client
from problems import views as problem_views
from problems.models import SpojProblem


class ProblemViewTest(TestCase):

    fixtures = ['test_auth.json', 'test_vnoiusers.json', 'test_problems.json', 'test_forum.json']

    def setUp(self):
        self.client = Client()
        self.problems_roads = SpojProblem.objects.get(code='ROADS')
        self.problems_nk05eopr = SpojProblem.objects.get(code='NK05EOPR')

    def test_url_resolve(self):
        # problem list
        resolver = resolve('/problems/list/')
        self.assertEqual(resolver.view_name, 'problems:list')
        self.assertEqual(resolver.func, problem_views.index)

        # problem show
        resolver = resolve('/problems/show/{}/'.format(self.problems_roads.code))
        self.assertEqual(resolver.view_name, 'problems:show')
        self.assertEqual(resolver.func, problem_views.show)

        # problem submit
        resolver = resolve('/problems/submit/{}/'.format(self.problems_roads.code))
        self.assertEqual(resolver.view_name, 'problems:submit')
        self.assertEqual(resolver.func, problem_views.submit)

        # problem status
        resolver = resolve('/problems/status/{}/'.format(self.problems_roads.code))
        self.assertEqual(resolver.view_name, 'problems:status')
        self.assertEqual(resolver.func, problem_views.status)

        # problem rank
        resolver = resolve('/problems/rank/{}/'.format(self.problems_roads.code))
        self.assertEqual(resolver.view_name, 'problems:rank')
        self.assertEqual(resolver.func, problem_views.rank)

        # problem discuss
        resolver = resolve('/problems/discuss/{}/'.format(self.problems_roads.code))
        self.assertEqual(resolver.view_name, 'problems:discuss')
        self.assertEqual(resolver.func, problem_views.discuss)

    def test_list_problems(self):
        response = self.client.get(reverse('problems:list'))
        self.assertEqual(response.status_code, 200)

    def test_load_problem(self):
        for problem in [self.problems_roads, self.problems_nk05eopr]:
            # Can show problem
            response = self.client.get(reverse('problems:show', kwargs={'code': problem.code}))
            self.assertEqual(response.status_code, 200)

            # When logged out, cannot submit problem
            response = self.client.get(reverse('problems:submit', kwargs={'code': problem.code}))
            self.assertRedirects(response, '/user/login?next=/problems/submit/{}/'.format(problem.code))
            # Login & check again
            self.login()
            response = self.client.get(reverse('problems:submit', kwargs={'code': problem.code}))
            self.assertEqual(response.status_code, 200)
            # We must logout to not affect other tests
            self.client.logout()

            # Problem status
            response = self.client.get(reverse('problems:status', kwargs={'code': problem.code}))
            self.assertEqual(response.status_code, 200)

            # Problem rank
            response = self.client.get(reverse('problems:rank', kwargs={'code': problem.code}))
            self.assertEqual(response.status_code, 200)

            # Problem discuss: Cannot discuss until login
            response = self.client.get(reverse('problems:discuss', kwargs={'code': problem.code}))
            self.assertRedirects(response, '/user/login?next=/problems/discuss/{}/'.format(problem.code))
            self.login()
            response = self.client.get(reverse('problems:discuss', kwargs={'code': problem.code}))
            self.assertEqual(response.status_code, 200)
            # We must logout to not affect other tests
            self.client.logout()

    def test_invalid_problem(self):
        # Show problem
        response = self.client.get('/problems/show/ABCD/')
        self.assertEqual(response.status_code, 404)

        # Problem status
        response = self.client.get('/problems/status/ABCD/')
        self.assertEqual(response.status_code, 404)

        # Problem rank
        response = self.client.get('/problems/rank/ABCD/')
        self.assertEqual(response.status_code, 404)

        # Submit problem
        self.login()
        response = self.client.get('/problems/submit/ABCD/')
        self.assertEqual(response.status_code, 404)

        # Problem discuss
        response = self.client.get('/problems/discuss/ABCD/')
        self.assertEqual(response.status_code, 404)

    def login(self):
        self.client.login(username='vnoiuser', password='vnoiuser')
