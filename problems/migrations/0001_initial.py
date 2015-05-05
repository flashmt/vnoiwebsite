# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '__first__'),
        ('vnoiusers', '__first__'),
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
                ('statement', django_bleach.models.BleachField(null=True)),
                ('author', models.CharField(max_length=250, null=True, blank=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('time_limit', models.FloatField(default=1)),
                ('source_limit', models.IntegerField(default=50000)),
                ('memory_limit', models.IntegerField(default=1536)),
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
            name='SpojProblemSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voj_account', models.CharField(max_length=100, null=True, blank=True)),
                ('submission_rank', models.IntegerField()),
                ('submission_id', models.IntegerField()),
                ('submission_data', models.DateField()),
                ('submission_verdict', models.CharField(max_length=200)),
                ('submission_time', models.FloatField()),
                ('submission_memory', models.CharField(max_length=50)),
                ('submission_language', models.CharField(max_length=50)),
                ('problem', models.ForeignKey(related_name='submissions', to='problems.SpojProblem')),
                ('vnoi_account', models.ForeignKey(related_name='submissions', blank=True, to='vnoiusers.VnoiUser', null=True)),
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
            field=models.ManyToManyField(related_name='+', null=True, to='problems.SpojProblemLanguage', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spojproblem',
            name='category',
            field=models.ForeignKey(related_name='problems', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='problems.SpojProblemCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spojproblem',
            name='cluster',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='problems.SpojCluster', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spojproblem',
            name='tags',
            field=models.ManyToManyField(related_name='problems', null=True, to='problems.SpojProblemTag', blank=True),
            preserve_default=True,
        ),
    ]
