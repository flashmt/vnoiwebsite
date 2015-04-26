# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django_bleach.models


class Migration(migrations.Migration):

    replaces = [(b'problems', '0001_initial'), (b'problems', '0002_auto_20150313_1837'), (b'problems', '0003_auto_20150319_1529'), (b'problems', '0004_spojproblemforum'), (b'problems', '0005_auto_20150407_1130'), (b'problems', '0006_auto_20150413_1216'), (b'problems', '0007_auto_20150413_1837'), (b'problems', '0008_auto_20150415_1533'), (b'problems', '0009_auto_20150415_1554'), (b'problems', '0010_auto_20150415_1608'), (b'problems', '0011_auto_20150415_1745')]

    dependencies = [
        ('forum', '0015_auto_20150327_1216'),
        ('vnoiusers', '0010_auto_20150327_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpojCluster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpojProblem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('problem_id', models.IntegerField()),
                ('name', models.CharField(max_length=250)),
                ('code', models.CharField(max_length=20)),
                ('accept_count', models.IntegerField(default=0)),
                ('accept_rate', models.FloatField(default=0.0)),
                ('score', models.FloatField(default=2.0)),
                ('_statement_rendered', models.TextField(null=True, editable=False, blank=True)),
                ('statement', models.TextField(null=True, blank=True)),
                ('author', models.CharField(max_length=250, null=True, blank=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('time_limit', models.FloatField(default=1)),
                ('source_limit', models.IntegerField(default=50000)),
                ('memory_limit', models.IntegerField(default=1536)),
                ('allowed_language', models.CharField(default=b'', max_length=1024)),
                ('problem_source', models.CharField(max_length=1024, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpojProblemCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='spojproblem',
            name='category',
            field=models.ForeignKey(related_name='problems', to='problems.SpojProblemCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spojproblem',
            name='cluster',
            field=models.ForeignKey(related_name='+', blank=True, to='problems.SpojCluster', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spojproblem',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='spojproblem',
            name='_statement_rendered',
        ),
        migrations.AlterField(
            model_name='spojproblem',
            name='statement',
            field=django_bleach.models.BleachField(null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='SpojProblemForum',
            fields=[
                ('forum_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='forum.Forum')),
                ('problem', models.ForeignKey(related_name='forum', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='problems.SpojProblem', null=True)),
            ],
            options={
            },
            bases=('forum.forum',),
        ),
        migrations.RemoveField(
            model_name='spojproblem',
            name='allowed_language',
        ),
        migrations.AlterField(
            model_name='spojproblem',
            name='category',
            field=models.ForeignKey(related_name='problems', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='problems.SpojProblemCategory', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spojproblem',
            name='cluster',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='problems.SpojCluster', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='SpojProblemLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('lang_id', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpojProblemTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='spojproblem',
            name='allowed_languages',
            field=models.ManyToManyField(related_name='+', null=True, to=b'problems.SpojProblemLanguage', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spojproblem',
            name='tags',
            field=models.ManyToManyField(related_name='problems', null=True, to=b'problems.SpojProblemTag', blank=True),
            preserve_default=True,
        ),
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
                ('verdict', models.CharField(max_length=200, null=True, blank=True)),
                ('raw_score', models.FloatField(default=0.0)),
                ('problem', models.ForeignKey(related_name='submissions', to='problems.SpojProblem')),
                ('participant', models.ForeignKey(related_name='submissions', blank=True, to='problems.SpojContestParticipant', null=True)),
                ('vnoi_account', models.ForeignKey(related_name='submissions', blank=True, to='vnoiusers.VnoiUser', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
