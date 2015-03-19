from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from forum.models import Forum, Topic, Post


class PostPermissionTest(TestCase):

    fixtures = ['auth.json', 'forum.json']

    def setUp(self):
        self.admin = User.objects.get(username="admin")

    def test_post_create_permission(self):
        # Test all authenticated user can create post
        pass

    def test_post_update_permission(self):
        # test only author can update post
        pass

