from avatar.models import Avatar
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save


class VnoiUser(models.Model):

    activation_key = models.CharField(max_length=40, blank=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile")
    dob = models.DateTimeField(null=True, blank=True)
    contribution = models.IntegerField(null=False, blank=False, default=0)
    voj_account = models.CharField(max_length=100, null=True, blank=True)
    codeforces_account = models.CharField(max_length=100, null=True, blank=True)
    topcoder_account = models.CharField(max_length=100, null=True, blank=True)
    topcoder_account_url = models.CharField(max_length=1024, null=True, blank=True)
    friends = models.ManyToManyField('self', related_name='+', symmetrical=False, null=True, blank=True)
    avatar = models.OneToOneField(Avatar, related_name="vnoiuser", null=True, blank=True)

    def __unicode__(self):
        return self.user.username


# Signals
def create_user_profile(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        return False
    if created:
        VnoiUser(user=instance).save()


post_save.connect(create_user_profile, sender=User)
