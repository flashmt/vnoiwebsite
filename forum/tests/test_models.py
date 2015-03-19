from django.test import TestCase

# Create your tests here.
from forum.models import Forum, Topic, Post


class ForumModelTest(TestCase):
    fixtures = ['forum.json', 'auth.json']

    def test_count_num_topics(self):
        self.assertEquals(Forum.objects.get(pk=1).count_num_topics(), 2)

    def test_count_num_posts(self):
        self.assertEquals(Forum.objects.get(pk=1).count_num_posts(), 7)

    def test_last_post(self):
        pass


class TopicModelTests(TestCase):
    fixtures = ['forum.json', 'auth.json']

    def test_delete(self):
        cf_294_topic = Topic.objects.get(pk=1)
        cf_forum = Forum.objects.get(pk=1)
        self.assertEquals(cf_forum.last_post.pk, 5)
        cf_294_topic.delete()
        cf_forum = Forum.objects.get(pk=1)
        self.assertEquals(cf_forum.last_post.pk, 5)


class PostModelTests(TestCase):
    fixtures = ['forum.json', 'auth.json']

    def test_delete(self):
        cf_294_topic_post = Post.objects.get(pk=5)
        self.assertEquals(cf_294_topic_post.topic.last_post.pk, 5)
        cm_1 = Post.objects.get(pk=7)
        cm_1.delete()
        cf_294_topic_post = Post.objects.get(pk=5)
        self.assertEquals(cf_294_topic_post.topic.last_post.pk, 6)
        cm_1 = Post.objects.get(pk=6)
        cm_1.delete()
        cf_294_topic_post = Post.objects.get(pk=5)
        self.assertEquals(cf_294_topic_post.topic.last_post.pk, 5)
