# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0005_auto_20150407_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpojProblemLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
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
        migrations.RemoveField(
            model_name='spojproblem',
            name='allowed_language',
        ),
        migrations.AddField(
            model_name='spojproblem',
            name='allowed_languages',
            field=models.ManyToManyField(related_name='+', null=True, to='problems.SpojProblemLanguage', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spojproblem',
            name='tags',
            field=models.ManyToManyField(related_name='problems', null=True, to='problems.SpojProblemTag', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spojproblemforum',
            name='problem',
            field=models.ForeignKey(related_name='forum', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='problems.SpojProblem', null=True),
            preserve_default=True,
        ),
    ]
