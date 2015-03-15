from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models

# Create your models here.


class VnoiUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile")
    dob = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    def is_admin(self):
        return Group.objects.get(name="Admin") in self.user.groups.all()
