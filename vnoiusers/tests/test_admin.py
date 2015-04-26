from django.test import TestCase


class UserAdminTest(TestCase):

    fixtures = ['test_auth.json', 'test_vnoiusers.json']

    def setUp(self):
        pass

    def test_admin_page(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/admin/vnoiusers/vnoiuser/')
        self.assertEqual(response.status_code, 200)
