from django.db import models

EXTERNAL_JUDGES = (
    ('cf', 'Codeforces'),
    ('tc', 'Topcoder'),
)


class ContestSchedule(models.Model):
    judge = models.CharField(max_length=2, choices=EXTERNAL_JUDGES)
    contest_name = models.CharField(max_length=255, null=False, blank=False)
    start_time = models.DateTimeField(null=False, blank=False)
    # Contest duration, in minutes
    duration = models.IntegerField(null=False, blank=False, default=120)
    url = models.CharField(max_length=1024, null=False, blank=False)

    def __unicode__(self):
        return self.contest_name