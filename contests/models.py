from django.db import models
from forum.models import Forum

# Create your models here.


class NonStandardContestStandingTable(models.Model):
    code = models.CharField(max_length=20, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    # Title of the standings (1d array, json)
    title = models.TextField(null=True, blank=True)
    # Content of the table (2d array, json)
    content = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return code + ' - ' + self.name


class NonStandardContestForum(Forum):
    contest = models.ForeignKey(NonStandardContestStandingTable, related_name='forum', null=True, blank=True, on_delete=models.SET_NULL)
