from datetime import timedelta
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.utils import timezone
from django_bleach.models import BleachField


class ForumGroup(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, related_name='forum_groups')

    ForumGroupChoices = (
        ('f', 'Forum'),
        ('l', 'Library')
    )
    group_type = models.CharField(max_length=3, choices=ForumGroupChoices, default='f')

    def __unicode__(self):
        return self.name


class Forum(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(default="")
    num_topics = models.IntegerField(default=0)
    num_posts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, related_name="created_forums")
    last_post = models.OneToOneField('Post', related_name="+", default=None, null=True, blank=True, on_delete=models.SET_NULL)
    forum_group = models.ForeignKey(ForumGroup, related_name="forums")

    def __unicode__(self):
        return self.name

    def update_last_post(self):
        for topic in self.topics.all():
            if (self.last_post is None) or ((topic.last_post is not None) and (self.last_post.created_at < topic.last_post.created_at)):
                self.last_post = topic.last_post
        self.save()

    def count_num_topics(self):
        return self.topics.all().count()

    def count_num_posts(self):
        num_posts = self.topics.all().aggregate(Sum('num_posts'))
        return num_posts['num_posts__sum'] or 0

    def get_last_post(self):
        """
        Scan over whole db to get the correct last_post.
        This method is inefficiently implemented, called only when needed.
        """
        last_posts = Post.objects.filter(topic__forum=self).order_by('-updated_at')
        return last_posts[0]

    def get_absolute_url(self):
        return reverse('forum:topic_list', kwargs={'forum_id': self.id})


class Topic(models.Model):
    forum = models.ForeignKey(Forum, related_name="topics")
    post = models.OneToOneField('Post', related_name="self_topic", null=True, blank=True)
    num_posts = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=500, null=False, blank=False)
    content = BleachField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, related_name="created_topics")
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name="updated_topics", null=True, default=None, on_delete=models.SET_NULL)
    last_post = models.OneToOneField('Post', related_name="+", null=True, blank=True, default=None, on_delete=models.SET_NULL)
    is_pinned = models.BooleanField(null=False, blank=False, default=False)

    def __unicode__(self):
        return self.title

    def get_last_post(self):
        """ This method query the whole db. Call it only when needed. """
        last_posts = Post.objects.filter(topic=self).order_by('-updated_at')
        if len(last_posts) > 0:
            return last_posts[0]
        else:
            return None

    def count_num_posts(self):
        return self.num_posts

    def get_absolute_url(self):
        return reverse('forum:topic_retrieve', kwargs={'forum_id': self.forum_id, 'topic_id': self.id})

    def get_total_vote(self):
        return self.post.num_upvotes - self.post.num_downvotes


class Post(models.Model):
    topic_post = models.BooleanField(default=False)
    # All post in the topic will point to this topic
    topic = models.ForeignKey(Topic, verbose_name='Topic', related_name='posts', null=True, on_delete=models.SET_NULL)
    # Point to the parent post. If the post is first post in topic, this will be None
    reply_on = models.ForeignKey("self", related_name="reply_posts", null=True, blank=True, on_delete=models.CASCADE)
    content = BleachField()
    num_upvotes = models.IntegerField(default=0)
    num_downvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, related_name="created_posts", null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name="updated_posts", default=None, null=True, on_delete=models.SET_NULL)
    # num_replies = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return self.content[:30]

    def total_votes(self):
        return self.num_upvotes - self.num_downvotes

    def title(self, parent_title=None):
        if self.topic_post:
            if parent_title is None:
                parent_title = self.topic.title
            return parent_title
        else:
            if parent_title is None:
                parent_title = self.reply_on.content[:10]
            return "Re: " + parent_title

    def get_reply_posts(self):
        return self.reply_posts.all()

    def count_num_replies(self):
        """This method query the whole db, use it only when needed """
        return self.posts.all().count()


class Vote(models.Model):
    UP_VOTE = 'u'
    DOWN_VOTE = 'd'

    VoteChoices = (
        (UP_VOTE, 'UpVote'),
        (DOWN_VOTE, 'DownVote')
    )
    type = models.CharField(max_length=5, choices=VoteChoices, default=UP_VOTE)
    post = models.ForeignKey(Post, related_name="votes")
    created_by = models.ForeignKey(User, related_name="votes")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return "{0} - {1} - {2}".format(self.type, self.post.id, self.created_by.username)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.type == self.UP_VOTE:
                self.post.num_upvotes += 1
            elif self.type == self.DOWN_VOTE:
                self.post.num_downvotes += 1

        self.post.save()
        super(Vote, self).save(*args, **kwargs)


# Django signals

def update_topic_on_save_post(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        return False
    topic = instance.topic
    if created:
        # If a new post was saved into database
        topic.num_posts += 1
        # Update topic.last_post
        topic.last_post = instance

    else:
        # On update an existing post
        if instance.topic_post:
            topic.content = instance.content
            topic.updated_at = instance.updated_at
            topic.updated_by = instance.updated_by
    topic.save()


def update_forum_on_save_post(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        return False
    forum = instance.topic.forum
    if created:
        forum.num_posts += 1
        # Update forum last_post
        forum.last_post = instance

    instance.topic.forum.save()


def update_forum_on_save_topic(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        return False
    if created:
        instance.forum.num_topics += 1

    instance.forum.save()


def update_forum_on_delete_topic(sender, instance, **kwargs):
    forum = instance.forum
    forum.num_topics -= 1
    forum.save()
    forum.update_last_post()


def update_topic_on_delete_post(sender, instance, auto_delete=False, **kwargs):
    topic_post = instance.topic_post
    topic = instance.topic

    for post in instance.reply_posts.all():
        post.delete(auto_delete=True)

    topic.num_posts -= 1
    topic.forum.num_posts -= 1
    if auto_delete is False:
        topic.last_post = topic.get_last_post()
        topic.save()

    if topic_post:
        topic.delete()


post_save.connect(update_topic_on_save_post, sender=Post)
post_save.connect(update_forum_on_save_post, sender=Post)
post_save.connect(update_forum_on_save_topic, sender=Topic)

post_delete.connect(update_topic_on_delete_post, sender=Post)
post_delete.connect(update_forum_on_delete_topic, sender=Topic)
