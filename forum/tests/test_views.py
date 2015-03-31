# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory
from forum.models import Post, Topic, Vote, Forum


class TopicViewTest(TestCase):

    fixtures = ['forum.json', 'auth.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.admin = User.objects.get(username="admin")

    def test_topic_create(self):
        self.client.login(username="admin", password="admin")
        post_content = "Nhớ thi nhé".decode('utf-8')
        topic = Topic(title="Codeforces round 295", content=post_content)
        response = self.client.post(reverse('forum:topic_create', kwargs={'forum_id': 1}),
                                    {'title': topic.title, 'content': topic.content})
        self.assertEquals(response.status_code, 302)
        # self.assertEquals(response['Location'], 'http://testserver/forum/1/4/')
        # self.assertEquals(Topic.objects.all().count(), 4)
        # self.assertEquals(Post.objects.all().count(), 9)
        # topic = Topic.objects.get(pk=4)
        # post = Post.objects.get(pk=9)
        forum = Forum.objects.get(pk=1)
        # check topic
        self.assertEquals(topic.content, post_content)
        # self.assertEquals(topic.num_posts, 1)
        # self.assertEquals(topic.created_by, self.admin)
        # self.assertEquals(topic.last_post, post)
        # self.assertEquals(topic.post, post)
        # self.assertEquals(topic.forum, forum)
        # check post
        # self.assertEquals(post.content, post_content)
        # self.assertEquals(post.created_by, self.admin)
        # self.assertEquals(post.topic_post, True)
        # self.assertEquals(post.self_topic, topic)
        # self.assertEquals(post.num_upvotes, 0)
        # self.assertEquals(post.num_downvotes, 0)
        # check forum
        # self.assertEquals(forum.num_posts, 8)
        # self.assertEquals(forum.last_post, post)

        # Ensure that non-existent forum throw a 404
        response = self.client.post(reverse('forum:topic_create', kwargs={'forum_id': 100}),
                                    {'title': topic.title, 'content': topic.content})
        self.assertEquals(response.status_code, 404)


class PostViewTest(TestCase):

    fixtures = ['forum.json', 'auth.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.admin = User.objects.get(username="admin")

    def test_post_create_level1(self):
        # Test create post (comment on topic)
        self.client.login(username="admin", password="admin")
        post = Post(content="huhu hôm nay bận mất rồi :(")
        response = self.client.post(reverse('forum:post_create', kwargs={'forum_id': 1, 'topic_id': 1, 'post_id': 1}), {'content': post.content})
        self.assertEquals(response.status_code, 302)
        # check post
        # self.assertEquals(Post.objects.all().count(), 9)
        # self.assertEquals(Post.objects.get(pk=1).reply_posts.all().count(), 3)
        # check topic
        # self.assertEquals(Topic.objects.all().count(), 3)
        # self.assertEquals(Topic.objects.get(pk=1).num_posts, 5)
        # self.assertEquals(Topic.objects.get(pk=1).last_post.id, 9)
        # check forum
        # self.assertEquals(Forum.objects.get(pk=1).num_posts, 8)
        # self.assertEquals(Forum.objects.get(pk=1).last_post.id, 9)

    def test_post_create_level2(self):
        # Test create post (comment on comment)
        self.client.login(username="admin", password="admin")
        post = Post(content="Mình cũng chắc chắn hehe")
        response = self.client.post(reverse('forum:post_create', kwargs={'forum_id': 1, 'topic_id': 1, 'post_id': 3}), {'content': post.content})
        self.assertEquals(response.status_code, 302)
        # self.assertEquals(Post.objects.all().count(), 9)
        # self.assertEquals(Post.objects.get(pk=3).reply_posts.all().count(), 1)
        # check topic
        # self.assertEquals(Topic.objects.all().count(), 3)
        # self.assertEquals(Topic.objects.get(pk=1).num_posts, 5)
        # self.assertEquals(Topic.objects.get(pk=1).last_post.id, 9)
        # check forum
        # self.assertEquals(Forum.objects.get(pk=1).num_posts, 8)
        # self.assertEquals(Forum.objects.get(pk=1).last_post.id, 9)

    def test_post_update_level0(self):
        # Test update topic
        self.client.login(username="admin", password="admin")
        post_data = {
            'title': "CF Round 294 tonight",
            'content': "Hôm nay 11h30 thi Codeforce nhé!!! Hihi yêu các bạn :P",
        }
        response = self.client.post(reverse('forum:post_update', kwargs={'forum_id': 1, 'topic_id': 1, 'post_id': 1}),
                                    {'title': post_data['title'], 'content': post_data['content']})
        self.assertEquals(response.status_code, 302)
        # self.assertEquals(Post.objects.all().count(), 8)
        post = Post.objects.get(pk=1)
        self.assertEquals(post.content, post_data['content'].decode('utf-8'))
        self.assertEquals(post.updated_by, self.admin)
        # check topic
        self.assertEquals(post.topic.id, 1)
        self.assertEquals(post.topic.updated_by, self.admin)
        # self.assertEquals(post.topic.num_posts, 4)
        # self.assertEquals(post.topic.last_post.id, 4)
        # check forum
        self.assertEquals(post.topic.forum.id, 1)
        # self.assertEquals(post.topic.forum.num_posts, 7)
        # self.assertEquals(post.topic.forum.last_post.id, 7)

    def test_post_update_level1(self):
        # Test update a comment of a topic
        pass

    def test_post_update_level2(self):
        # Test update a comment of a comment
        pass


class VoteViewTest(TestCase):

    fixtures = ['auth.json', 'forum.json', 'vnoiusers.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_vote_create_successfully(self):
        self.client.login(username="admin", password="admin")

        # Test successfully create upvote
        response = self.client.get(reverse('forum:vote_create', kwargs={'post_id': 1}), {'type': Vote.UP_VOTE})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Post.objects.get(pk=1).num_upvotes, 1)
        self.assertEquals(Post.objects.get(pk=1).num_downvotes, 0)

        # Test successfully create downvote
        response = self.client.get(reverse('forum:vote_create', kwargs={'post_id': 2}), {'type': Vote.DOWN_VOTE})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Post.objects.get(pk=2).num_upvotes, 0)
        self.assertEquals(Post.objects.get(pk=2).num_downvotes, 1)

    def test_vote_create_unsuccessfully(self):
        # if user already vote this post
        self.client.login(username="admin", password="admin")
        self.client.get(reverse('forum:vote_create', kwargs={'post_id': 1}), {'type': Vote.UP_VOTE})

        response = self.client.get(reverse('forum:vote_create', kwargs={'post_id': 1}), {'type': Vote.UP_VOTE})
        self.assertEqual(
            response.__dict__['_container'],
            ['{"message": "You already voted", "success": 0}'])

        response = self.client.get(reverse('forum:vote_create', kwargs={'post_id': 1}), {'type': Vote.DOWN_VOTE})
        self.assertEqual(
            response.__dict__['_container'],
            ['{"message": "You already voted", "success": 0}'])

        # If user doesn't have permission
        pass


