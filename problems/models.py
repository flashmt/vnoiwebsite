from django.db import models
from django_bleach.models import BleachField
from forum.models import Forum
from vnoiusers.models import VnoiUser


class SpojContest(models.Model):
    code = models.CharField(max_length=20, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)

    def __unicode__(self):
        return self.name

    def get_standings(self):
        return self.participants.all().order_by('-get_total_score')


class SpojContestParticipant(models.Model):
    contest = models.ForeignKey(SpojContest, related_name='participants', null=False, blank=False)
    # cache name
    name = models.CharField(max_length=250, null=False, blank=False)

    # calculate total score of last submissions (each problem)
    def get_total_score(self):
        calculated = []
        total_score = 0
        for submission in self.submissions.all().order_by('-submit_time'):
            if submission.problem.code in calculated:
                continue
            calculated.append(submission.problem.code)
            total_score = total_score + submission.get_actual_score(is_contest=True)
        return total_score


class SpojProblemCategory(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __unicode__(self):
        return self.name


class SpojCluster(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name


class SpojProblemTag(models.Model):
    name = models.CharField(max_length=20, null=True, blank=False)

    def __unicode__(self):
        return self.name


class SpojProblemLanguage(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    lang_id = models.IntegerField(null=False, blank=False)

    def __unicode__(self):
        return self.name


class SpojProblem(models.Model):
    # contest that contain this problem
    contest = models.ForeignKey(SpojContest, related_name='problems', null=True, blank=True, on_delete=models.SET_NULL)
    # coefficient of this problem in the above contest
    coefficient = models.FloatField(null=False, blank=False, default=1.0)

    category = models.ForeignKey(SpojProblemCategory, related_name='problems', null=True, blank=True, on_delete=models.SET_NULL)
    problem_id = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    code = models.CharField(max_length=20, null=False, blank=False)
    accept_count = models.IntegerField(null=False, blank=False, default=0)
    accept_rate = models.FloatField(null=False, blank=False, default=0.0)
    score = models.FloatField(null=False, blank=False, default=2.0)
    statement = BleachField(null=True,
                            allowed_tags=[
                                'p', 'strong', 'em', 'pre', 'code', 'a', 'img', 'ol', 'ul', 'li', 'span', 'i', 'sub',
                                'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'sub', 'sup'
                            ],
                            allowed_attributes=['href', 'class', 'alt', 'style', 'src'],
                            strip_tags=False)
    author = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateField(null=True, blank=True, auto_now_add=True)
    # Time limit in second
    time_limit = models.FloatField(null=False, blank=False, default=1)
    # Source code limit in bytes
    source_limit = models.IntegerField(null=False, blank=False, default=50000)
    # Memory limit in MB
    memory_limit = models.IntegerField(null=False, blank=False, default=1536)
    # Allowed languages
    allowed_languages = models.ManyToManyField(SpojProblemLanguage, related_name='+', null=True, blank=True)
    # Problem's tags
    tags = models.ManyToManyField(SpojProblemTag, related_name='problems', null=True, blank=True)
    # Problem's source
    problem_source = models.CharField(max_length=1024, blank=True, null=True)
    # Cluster (doesn't need anymore)
    cluster = models.ForeignKey(SpojCluster, related_name='+', null=True, blank=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name


class SpojProblemSubmission(models.Model):
    row = models.ForeignKey(SpojContestParticipant, related_name='submissions', null=True, blank=True)
    problem = models.ForeignKey(SpojProblem, related_name='submissions', null=False, blank=False)

    voj_account = models.CharField(max_length=100, null=True, blank=True)
    vnoi_account = models.ForeignKey(VnoiUser, related_name='submissions', null=True, blank=True)

    submission_id = models.IntegerField(null=False, blank=False)
    submit_time = models.DateField(null=False, blank=False)
    verdict = models.CharField(max_length=50, null=True, blank=True)
    raw_score = models.FloatField(null=False, blank=False, default=0.0)

    def get_actual_score(self, is_contest=False):
        if is_contest:
            if self.problem.category.name is 'acm':
                # check error < 10^-4
                if abs(self.raw_score - 1.0) < 1e-4:
                    return self.problem.coefficient
                else:
                    return 0
            else:
                return self.raw_score * self.problem.coefficient
        else:
            if self.problem.category.name is 'acm':
                # check error < 10^-4
                if abs(self.raw_score - 1.0) < 1e-4:
                    return self.raw_score * self.problem.score
                else:
                    return 0
            else:
                return self.raw_score * self.problem.score


class SpojProblemForum(Forum):
    # Assumption: forum name must be equal to problem code.
    # This is used in get_absolute_url in forum.models.Forum
    problem = models.ForeignKey(SpojProblem, related_name='forum', null=True, blank=True, on_delete=models.SET_NULL)
