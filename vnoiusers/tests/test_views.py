from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.contrib.auth.models import User
from vnoiusers import views


class UserProfileTest(TestCase):

    fixtures = ['forum.json', 'auth.json', 'vnoiusers.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_user_profile(self):

        user = User.objects.create(
            username="khoa",
            password="khoa",
            first_name="test",
            email="test@test.vn"
        )

        response = self.client.get(reverse('user:profile', kwargs={'user_id': user.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'test@test.vn')
        self.assertContains(response, 'test')

        self.client.login(username="admin", password="admin")
        response = self.client.get(
            reverse(
                'user:profile',
                kwargs={'user_id': 1}
            )
        )
        self.assertEquals(response.context['is_authenticated'], True)

        response = self.client.get(
            reverse(
                'user:profile',
                kwargs={'user_id': user.pk}
            )
        )
        self.assertEquals(response.context['is_authenticated'], False)

        count = User.objects.count()
        response = self.client.get(
            reverse(
                'user:profile',
                kwargs={'user_id': (count+1)}
            )
        )
        self.assertEqual(response.status_code, 404)
