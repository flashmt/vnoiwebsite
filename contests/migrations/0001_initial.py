# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='NonStandardContestForum',
            fields=[
                ('forum_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='forum.Forum')),
            ],
            options={
            },
            bases=('forum.forum',),
        ),
        migrations.CreateModel(
            name='NonStandardContestStandingTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=250)),
                ('title', models.TextField(null=True, blank=True)),
                ('content', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='nonstandardcontestforum',
            name='contest',
            field=models.ForeignKey(related_name='forum', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='contests.NonStandardContestStandingTable', null=True),
            preserve_default=True,
        ),
    ]
