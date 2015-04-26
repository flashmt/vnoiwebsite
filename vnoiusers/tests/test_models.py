from django.contrib.auth.models import User
from django.test import TestCase
from vnoiusers.user_util import is_admin


class UserViewTest(TestCase):

    fixtures = ['test_auth.json', 'test_vnoiusers.json']

    def setUp(self):
        pass

    def test_create_user_profile(self):
        username = 'test_create_user_RR'
        user = User.objects.create(username=username, password='12345')
        user.save()

        # I have no idea what I am doing here
        profile = user.profile
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.__unicode__(), username)

    def test_is_admin(self):
        user_admin = User.objects.get(username='admin')
        self.assertTrue(is_admin(user_admin))

        user_vnoi = User.objects.get(username='vnoiuser')
        self.assertFalse(is_admin(user_vnoi))
