from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class ForumGroup(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, related_name='forum_groups')

    def __unicode__(self):
        return self.name


class Forum(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(default="")

    num_topics = models.IntegerField(default=0)
    num_posts = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, related_name="created_forums")
    
    last_post = models.OneToOneField('Post', related_name="+", default=None, null=True, blank=True)

    forum_group = models.ForeignKey(ForumGroup, related_name="forums")

    def __unicode__(self):
        return self.name

    def count_num_topics(self):
        return self.num_topics

    def count_num_posts(self):
        return self.num_posts

    def get_last_post(self):
        return self.last_post

class Topic(models.Model):
    forum = models.ForeignKey(Forum, related_name="topics")
    post = models.ForeignKey('Post', related_name="topics", null=True, blank=True)
    num_posts = models.PositiveSmallIntegerField(verbose_name="num_replies", default=0)
    title = models.CharField(max_length=500, null=False, blank=False)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, related_name="created_topics")

    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name="updated_topics", default=None)

    last_post = models.OneToOneField('Post', related_name="+", default=None, null=True, blank=True)

    # TODO created_by, updated_at, level

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk: # New topic
            self.forum.num_topics += 1            
        else: # Edited topic
            self.forum.last_post = self.last_post;          
        self.forum.save()

        super(Topic, self).save(*args, **kwargs)

    def count_num_posts(self):
        return self.num_posts


class Post(models.Model):
    topic_post = models.BooleanField(default=False)
    topic = models.ForeignKey(Topic, verbose_name='Topic', related_name='posts')
    reply_on = models.ForeignKey("self", related_name="reply_posts", null=True, blank=True)
    content = models.TextField(null=False, blank=False)
    num_votes = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, related_name="created_posts")

    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name="updated_posts", default=None)
  
    # TODO: created_by, updated_by

    def __unicode__(self):
        return self.content[:30]

    def save(self, *args, **kwargs):
        if not self.pk: # New post
            self.topic.num_posts += 1
            self.topic.created_by = self.created_by
            self.topic.created_at = self.created_at
            self.topic.updated_at = self.updated_at
            self.topic.updated_by = self.updated_by
            self.topic.save()

            self.topic.forum.num_posts += 1            
            self.topic.forum.save()
        else: # Edited post
            if self.topic_post: # Edited content
                self.topic.content = self.content

            self.topic.updated_at = self.updated_at
            self.topic.updated_by = self.updated_by
            self.topic.save()

        super(Post, self).save(*args, **kwargs)
        # Assign last_post
        self.topic.last_post = self;
        self.topic.save()

    def title(self):
        if self.topic_post:
            return self.topic.title
        else:
            return "Re: " + self.reply_on.content[:10]

    def get_reply_posts(self):
        return self.reply_posts.all()