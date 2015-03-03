# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory
from forum.models import Post, Topic, Vote


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


class VoteViewTest(TestCase):

    fixtures = ['auth.json', 'forum.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_vote_create_successfully(self):
        self.client.login(username="admin", password="admin")

        # Test successfully create upvote
        response = self.client.get(reverse('forum:vote_create', kwargs={'post_id': 1}), {'type': Vote.UPVOTE})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Post.objects.get(pk=1).num_upvotes, 1)
        self.assertEquals(Post.objects.get(pk=1).num_downvotes, 0)

        # Test successfully create downvote
        response = self.client.get(reverse('forum:vote_create', kwargs={'post_id': 2}), {'type': Vote.DOWNVOTE})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Post.objects.get(pk=2).num_upvotes, 0)
        self.assertEquals(Post.objects.get(pk=2).num_downvotes, 1)

    def test_vote_create_unsuccessfully(self):
        # if user already vote this post
        self.client.login(username="admin", password="admin")
        self.client.get(reverse('forum:vote_create', kwargs={'post_id': 1}), {'type': Vote.UPVOTE})

        response = self.client.get(reverse('forum:vote_create', kwargs={'post_id': 1}), {'type': Vote.UPVOTE})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, 'User already voted this post')
        self.assertEquals(response.context, None)

        response = self.client.get(reverse('forum:vote_create', kwargs={'post_id': 1}), {'type': Vote.DOWNVOTE})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, 'User already voted this post')
        self.assertEquals(response.context, None)

        # If user doesn't have permission
        pass


