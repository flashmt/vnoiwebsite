from django.db import models
from forum.models import Forum

# Create your models here.


class ContestStandingTable(models.Model):
    code = models.CharField(max_length=20, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)

    # Title of the standings (1d array, json)
    # e.g.   Rank | Handle | Name    | Problem A | Problem B | ...
    title = models.TextField(null=True, blank=True)

    # Content of the table (2d array, json)
    # e.g. { 1    | nobita | Nobita  | 100       | 100       | ...,
    #        2    | chaien | Takeshi | 90        | 90        | ...,
    #        3    | xuka   | Shizuka | 90        | 50        | ... }
    content = models.TextField(null=True, blank=True)


class ContestForum(Forum):
    contest = models.ForeignKey(ContestStandingTable, related_name='forum', null=True, blank=True, on_delete=models.SET_NULL)
