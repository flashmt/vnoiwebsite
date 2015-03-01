# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [(b'forum', '0001_initial'), (b'forum', '0002_auto_20150228_1706'), (b'forum', '0003_auto_20150228_1720'), (b'forum', '0004_auto_20150228_1721'), (b'forum', '0005_auto_20150228_1725'), (b'forum', '0006_auto_20150228_1758'), (b'forum', '0002_auto_20150228_1749'), (b'forum', '0007_merge'), (b'forum', '0008_auto_20150301_1711')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(default=b'')),
                ('num_topics', models.IntegerField(default=0)),
                ('num_posts', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(related_name='created_forums', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic_post', models.BooleanField(default=False)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('num_votes', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(related_name='created_posts', to=settings.AUTH_USER_MODEL)),
                ('reply_on', models.ForeignKey(related_name='reply_posts', blank=True, to='forum.Post', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_posts', models.PositiveSmallIntegerField(default=0, verbose_name=b'num_replies')),
                ('title', models.CharField(max_length=500)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(related_name='created_topics', to=settings.AUTH_USER_MODEL)),
                ('forum', models.ForeignKey(related_name='topics', to='forum.Forum')),
                ('post', models.ForeignKey(related_name='topics', blank=True, to='forum.Post', null=True)),
                ('last_post', models.OneToOneField(related_name='+', null=True, default=None, blank=True, to='forum.Post')),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_by', models.ForeignKey(related_name='updated_topics', default=None, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(related_name='posts', verbose_name=b'Topic', to='forum.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='last_post',
            field=models.OneToOneField(related_name='+', null=True, default=None, blank=True, to='forum.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_posts', default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forum',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ForumGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('created_by', models.ForeignKey(related_name='forum_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='forum',
            name='forum_group',
            field=models.ForeignKey(related_name='forums', to='forum.ForumGroup'),
            preserve_default=True,
        ),
    ]
