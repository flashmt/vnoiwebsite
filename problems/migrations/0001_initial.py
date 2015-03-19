# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
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
    ]
