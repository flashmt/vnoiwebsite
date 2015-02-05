from django.test import TestCase
from django.test.client import Client, RequestFactory
from forum.forms import PostCreateForm
from forum.models import Post


class PostViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.post = Post()
        # login before act
        self.client.login(username="admin", password="admin")

    def test_post_create(self):
        form = PostCreateForm(instance=self.post)
        response = self.client.post('/forum/post_create/', {'form': form})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Post.objects.all().count, 4)

    def test_post_update(self):
        pass
