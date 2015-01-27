from django.db import models

# Create your models here.

class Thread(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    parent_thread = models.ForeignKey(Thread, null=True, blank=True, related_name="children_comment")
    parent_comment = models.ForeignKey("self", null=True, blank=True, related_name="children_comment")
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    num_of_vote = models.IntegerField(default=0)


