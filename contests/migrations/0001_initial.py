# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContestForum',
            fields=[
                ('forum_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='forum.Forum')),
                ('contest', models.ForeignKey(related_name='forum', blank=True, to='contests.Contest', null=True)),
            ],
            options={
            },
            bases=('forum.forum',),
        ),
        migrations.CreateModel(
            name='ContestGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContestResource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('display_order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContestExtraLink',
            fields=[
                ('contestresource_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='contests.ContestResource')),
                ('url', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=('contests.contestresource',),
        ),
        migrations.CreateModel(
            name='ContestStanding',
            fields=[
                ('contestresource_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='contests.ContestResource')),
                ('title', models.TextField(null=True, blank=True)),
                ('content', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=('contests.contestresource',),
        ),
        migrations.AddField(
            model_name='contestresource',
            name='contest',
            field=models.ForeignKey(related_name='resources', to='contests.Contest'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contest',
            name='group',
            field=models.ForeignKey(related_name='contests', to='contests.ContestGroup'),
            preserve_default=True,
        ),
    ]