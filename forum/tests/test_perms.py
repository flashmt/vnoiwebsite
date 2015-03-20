from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from forum.models import Forum, Topic, Post
from forum.perms import PostPermission


class PostPermissionTest(TestCase):

    fixtures = ['auth.json', 'forum.json', 'vnoiusers.json']

    def setUp(self):
        self.admin = User.objects.get(username="admin")
        self.vnoiuser = User.objects.get(username="vnoiuser")
        self.admin_post = Post.objects.filter(created_by_id=1)[0]
        self.vnoiuser_post = Post.objects.filter(created_by_id=2)[0]

    def test_post_create_permission(self):
        # Test all authenticated user can create post
        self.assertTrue(PostPermission(self.admin).can_create_post())
        self.assertTrue(PostPermission(self.admin).can_create_post)

    def test_post_update_permission(self):
        # test admin or author can update post
        self.assertTrue(PostPermission(self.admin).can_update_post(self.vnoiuser_post))
        self.assertTrue(PostPermission(self.admin).can_update_post(self.admin_post))
        self.assertFalse(PostPermission(self.vnoiuser).can_update_post(self.admin_post))
