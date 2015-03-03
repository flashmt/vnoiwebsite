# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory
from forum.models import Post, Topic


class TopicViewTest(TestCase):

    fixtures = ['forum.json', 'auth.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_topic_create(self):
        self.client.login(username="admin", password="admin")
        topic = Topic(title="Codeforces round 295", content="Nhớ thi nhé :D")
        response = self.client.post(reverse('forum:topic_create', kwargs={'forum_id': 1}),
                                    {'title': topic.title, 'content': topic.content})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['Location'], 'http://testserver/forum/1/3/')
        self.assertEquals(Topic.objects.all().count(), 3)
        self.assertEquals(Post.objects.all().count(), 8)
        self.assertEquals(Topic.objects.get(pk=3).content, topic.content.decode('utf-8'))
        self.assertEquals(Post.objects.get(pk=8).content, topic.content.decode('utf-8'))

        # Ensure that non-existent forum throw a 404
        response = self.client.post(reverse('forum:topic_create', kwargs={'forum_id': 100}),
                                    {'title': topic.title, 'content': topic.content})
        self.assertEquals(response.status_code, 404)


class PostViewTest(TestCase):

    fixtures = ['forum.json', 'auth.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_post_create(self):
        self.client.login(username="admin", password="admin")

        # Test create post (comment on topic)
        post = Post(content="huhu hôm nay bận mất rồi :(")
        response = self.client.post(reverse('forum:post_create', kwargs={'forum_id': 1, 'topic_id': 1, 'post_id': 1}), {'content': post.content})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Post.objects.all().count(), 8)
        self.assertEquals(Post.objects.get(pk=1).reply_posts.all().count(), 3)

        # Test create post (comment on comment)
        post = Post(content="Mình cũng chắc chắn hehe")
        response = self.client.post(reverse('forum:post_create', kwargs={'forum_id': 1, 'topic_id': 1, 'post_id': 3}), {'content': post.content})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Post.objects.all().count(), 9)
        self.assertEquals(Post.objects.get(pk=3).reply_posts.all().count(), 1)

    def test_post_update(self):
        self.client.login(username="admin", password="admin")
        pass
