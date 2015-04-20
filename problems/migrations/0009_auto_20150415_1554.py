# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vnoiusers', '0010_auto_20150327_1604'),
        ('problems', '0008_auto_20150415_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpojContestParticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('contest', models.ForeignKey(related_name='participants', to='problems.SpojContest')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpojProblemSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voj_account', models.CharField(max_length=100, null=True, blank=True)),
                ('submission_id', models.IntegerField()),
                ('submit_time', models.DateField()),
                ('verdict', models.CharField(max_length=50, null=True, blank=True)),
                ('raw_score', models.FloatField(default=0.0)),
                ('problem', models.ForeignKey(related_name='submissions', to='problems.SpojProblem')),
                ('row', models.ForeignKey(related_name='submissions', blank=True, to='problems.SpojContestParticipant', null=True)),
                ('vnoi_account', models.ForeignKey(related_name='submissions', blank=True, to='vnoiusers.VnoiUser', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='spojconteststandingrow',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='spojproblemscore',
            name='problem',
        ),
        migrations.RemoveField(
            model_name='spojproblemscore',
            name='row',
        ),
        migrations.DeleteModel(
            name='SpojContestStandingRow',
        ),
        migrations.RemoveField(
            model_name='spojproblemscore',
            name='vnoi_account',
        ),
        migrations.DeleteModel(
            name='SpojProblemScore',
        ),
    ]
