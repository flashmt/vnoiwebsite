from django.test import TestCase

# Create your tests here.
from forum.models import Forum


class ForumModelTest(TestCase):
    fixtures = ['forum.json', 'auth.json']

    def test_count_num_topics(self):
        self.assertEquals(Forum.objects.get(pk=1).count_num_topics(), 2)

    def test_count_num_posts(self):
        self.assertEquals(Forum.objects.get(pk=1).count_num_posts(), 7)

    def test_last_post(self):
        pass


class TopicModelTests(TestCase):
    pass


