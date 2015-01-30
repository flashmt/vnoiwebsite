from django.conf import settings
from django.db import models

# Create your models here.

class VnoiUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    dob = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.user.username


