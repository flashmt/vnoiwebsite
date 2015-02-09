from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Sum


class Forum(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(default='')
    num_topics = models.IntegerField(default=0)
    num_posts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="created_forums")

    def __unicode__(self):
        return self.name

    def count_num_topics(self):
        return self.topics.all().count()

    def count_num_posts(self):
        num_posts = 0
        for topic in self.topics.all():
        	num_posts = num_posts + topic.count_num_posts()
        return num_posts

    def last_post(self):
        if self.topics.all().count:
            last_post = Post.objects.all().filter(topic__forum=self).order_by("-created_at")[0]
            return last_post
        else:
            return None


class Topic(models.Model):
    forum = models.ForeignKey(Forum, related_name="topics")
    post = models.ForeignKey('Post', related_name="topics", null=True, blank=True)
    num_posts = models.PositiveSmallIntegerField(verbose_name="num_replies", default=0)
    title = models.CharField(max_length=500, null=False, blank=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="created_topics")

    # TODO created_by, updated_at, level

    def __unicode__(self):
        return self.title

    def count_num_posts(self):
        return self.posts.all().count()

    def last_post(self):
        if self.posts.all().count:
            return self.posts.order_by("-created_at")[0]
        else:
            return None


class Post(models.Model):
    topic_post = models.BooleanField(default=False)
    topic = models.ForeignKey(Topic, verbose_name='Topic', related_name='posts')
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="created_posts")
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    num_votes = models.IntegerField(default=0)
    reply_on = models.ForeignKey("self", related_name="reply_posts", null=True, blank=True)

    # TODO: created_by, updated_by

    def __unicode__(self):
        return self.content[:30]

    def title(self):
        if self.topic_post:
            return self.topic.title
        else:
            return "Re: " + self.reply_on.content[:10]
