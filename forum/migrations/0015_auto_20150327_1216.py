# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0014_forumgroup_group_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='reply_on',
            field=models.ForeignKey(related_name='reply_posts', blank=True, to='forum.Post', null=True),
            preserve_default=True,
        ),
    ]
