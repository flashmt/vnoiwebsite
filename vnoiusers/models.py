from avatar.models import Avatar
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models

# Create your models here.


class VnoiUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile")
    dob = models.DateField(null=True, blank=True)
    contribution = models.IntegerField(null=False, blank=False, default=0)
    voj_account = models.CharField(max_length=100, null=True, blank=True)
    codeforces_account = models.CharField(max_length=100, null=True, blank=True)
    topcoder_account = models.CharField(max_length=100, null=True, blank=True)
    topcoder_account_url = models.CharField(max_length=1024, null=True, blank=True)
    friends = models.ManyToManyField('self', related_name='+', symmetrical=False)
    avatar = models.OneToOneField(Avatar, related_name="vnoiuser", null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    def is_admin(self):
        return Group.objects.get(name="Admin") in self.user.groups.all()