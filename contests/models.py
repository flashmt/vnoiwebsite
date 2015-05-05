from django.db import models
from forum.models import Forum


class ContestGroup(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False)

    def __str__(self):
        return self.name


class Contest(models.Model):
    class Meta:
        ordering = ['name']

    code = models.CharField(max_length=20, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    group = models.ForeignKey(ContestGroup, related_name='contests', on_delete=models.CASCADE)

    def __str__(self):
        return self.code + ' - ' + self.name


class ContestResource(models.Model):
    class Meta:
        ordering = ['name']

    contest = models.ForeignKey(Contest, related_name='resources', on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False, blank=False)

    # This field is used for sorting resources inside a contest
    # Default = 0 --> any order can appear / make sense
    display_order = models.IntegerField(default=0, null=False, blank=False)


class ContestStanding(ContestResource):
    # Title of the standings (1d array, json)
    # e.g.   { "Rank ", " Handle ", " Name    ", " Problem A ", " Problem B ", ...}
    title = models.TextField(null=True, blank=True)

    # Content of the table (2d array, json)
    # e.g.  {{ "1    ", " nobita ", " Nobita  ", " 100       ", " 100       ", ...},
    #        { "2    ", " chaien ", " Takeshi ", " 90        ", " 90        ", ...},
    #        { "3    ", " xuka   ", " Shizuka ", " 90        ", " 50        ", ...}}
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.contest.code + ' - ' + self.name


class ContestExtraLink(ContestResource):
    url = models.CharField(max_length=1000, null=False, blank=False)

    def __str__(self):
        return self.name


class ContestForum(Forum):
    contest = models.ForeignKey(Contest, related_name='forum', null=True, blank=True, on_delete=models.CASCADE)
