# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_pinnedtopic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pinnedtopic',
            name='topic',
        ),
        migrations.AddField(
            model_name='pinnedtopic',
            name='post',
            field=models.ForeignKey(related_name='+', default=None, to='forum.Post'),
            preserve_default=False,
        ),
    ]
