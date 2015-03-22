from django.test import TestCase

# Create your tests here.
from forum.models import Forum, Topic, Post
from django.contrib.auth.models import User

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
        forum = Forum.objects.get(id=1)
        forum.update_last_post()
        old_id = forum.last_post.id

        user = User.objects.get(id=1)
        topic = forum.topics.create(created_by = user, updated_by = 
user)
        post = topic.posts.create(created_by = user, updated_by = user)
new_id = post.id			
        self.assertEquals(forum.last_post.id, new_id)
        topic.delete()
        self.assertEquals(forum.last_post.id, old_id)	

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
