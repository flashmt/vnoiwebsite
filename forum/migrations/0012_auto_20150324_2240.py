# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_pinnedtopic_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pinnedtopic',
            name='author',
        ),
        migrations.RemoveField(
            model_name='pinnedtopic',
            name='content',
        ),
        migrations.RemoveField(
            model_name='pinnedtopic',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='pinnedtopic',
            name='forum_id',
        ),
        migrations.RemoveField(
            model_name='pinnedtopic',
            name='is_cached',
        ),
        migrations.RemoveField(
            model_name='pinnedtopic',
            name='last_updated',
        ),
        migrations.RemoveField(
            model_name='pinnedtopic',
            name='post',
        ),
        migrations.RemoveField(
            model_name='pinnedtopic',
            name='topic_id',
        ),
        migrations.RemoveField(
            model_name='pinnedtopic',
            name='topic_title',
        ),
        migrations.RemoveField(
            model_name='pinnedtopic',
            name='total_vote',
        ),
        migrations.AddField(
            model_name='pinnedtopic',
            name='topic',
            field=models.ForeignKey(related_name='+', default=None, to='forum.Topic'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='topic',
            name='num_posts',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='post',
            field=models.OneToOneField(related_name='self_topic', null=True, blank=True, to='forum.Post'),
            preserve_default=True,
        ),
    ]
