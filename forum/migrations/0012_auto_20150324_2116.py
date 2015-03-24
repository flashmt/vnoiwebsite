# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_pinnedtopic_created_at'),
    ]

    operations = [
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
