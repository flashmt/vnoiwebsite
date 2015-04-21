# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vnoiusers', '0010_auto_20150327_1604'),
        ('problems', '0007_auto_20150413_1837'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpojContest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpojContestStandingRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('contest', models.ForeignKey(related_name='standings', to='problems.SpojContest')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpojProblemScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voj_account', models.CharField(max_length=100, null=True, blank=True)),
                ('raw_score', models.FloatField(default=0.0)),
                ('problem', models.ForeignKey(related_name='standings', to='problems.SpojProblem')),
                ('row', models.ForeignKey(related_name='scores', to='problems.SpojContestStandingRow')),
                ('vnoi_account', models.ForeignKey(related_name='standings', blank=True, to='vnoiusers.VnoiUser', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='spojproblem',
            name='coefficient',
            field=models.FloatField(default=1.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spojproblem',
            name='contest',
            field=models.ForeignKey(related_name='problems', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='problems.SpojContest', null=True),
            preserve_default=True,
        ),
    ]
