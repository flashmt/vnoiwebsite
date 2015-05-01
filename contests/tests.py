from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.test import Client
import mock

# Create your tests here.


class ContestViewTest(TestCase):

    fixtures = ['auth.json', 'contests.json']

    def setUp(self):
        self.client = Client()

    def test_contest_view(self):
        response = self.client.get(reverse('contests:show_table', kwargs={'contest_id': 1}))
        self.assertEquals(response.status_code, 200)

        response = self.client.get(reverse('contests:show_table', kwargs={'contest_id': 999}))
        self.assertEquals(response.status_code, 404)
