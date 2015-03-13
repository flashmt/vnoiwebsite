from django.db import models
from precise_bbcode.fields import BBCodeTextField


class SpojProblemCategory(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __unicode__(self):
        return self.name


class SpojCluster(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name


class SpojProblem(models.Model):
    category = models.ForeignKey(SpojProblemCategory, related_name='problems', null=False, blank=False)
    id = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    code = models.CharField(max_length=20, null=False, blank=False)
    accept_count = models.IntegerField(null=False, blank=False, default=0)
    accept_rate = models.FloatField(null=False, blank=False, default=0.0)
    score = models.FloatField(null=False, blank=False, default=2.0)
    statement = BBCodeTextField()
    author = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateField(null=False, blank=False, auto_now_add=True)
    time_limit = models.FloatField(null=False, blank=False, default=1)
    source_limit = models.IntegerField(null=False, blank=False, default=50000)
    memory_limit = models.IntegerField(null=False, blank=False, default=1536)
    allowed_language = models.CharField(max_length=1024, blank=False, null=False, default='Tất cả')
    problem_source = models.CharField(max_length=1024, blank=False, ull=False)
    cluster = models.ForeignKey(SpojCluster, related_name='+')

    def __unicode__(self):
        return self.name