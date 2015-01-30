from django.db import models

# Create your models here.
from django.db.models import Max, Sum


class Forum(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(default='')
    num_topics = models.IntegerField(default=0)
    num_posts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def count_num_topics(self):
        return self.topics.all().count

    def count_num_posts(self):
        num_posts = self.topics.all().aggregate(Sum('num_posts'))
        return num_posts['num_posts__sum'] or 0


class Topic(models.Model):
    forum = models.ForeignKey(Forum, related_name="topics")
    post = models.ForeignKey('Post', related_name="topics")
    num_posts = models.PositiveSmallIntegerField(verbose_name="num_replies", default=0)
    title = models.CharField(max_length=500, null=False, blank=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    #TODO created_by, updated_at, level

    def __unicode__(self):
        return self.title

    def count_num_posts(self):
        return self.posts.all().count()


class Post(models.Model):
    topic_post = models.BooleanField(default=False)
    topic = models.ForeignKey(Topic, verbose_name='Topic', related_name='posts')
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    num_votes = models.IntegerField(default=0)
    reply_on = models.ForeignKey("self", related_name="reply_posts", default='0')
    #TODO: created_by, updated_by

    def __unicode__(self):
        return self.content[:30]

    def title(self):
        if self.topic_post:
            return self.topic.title
        else:
            return "No need title"
