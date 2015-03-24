# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0012_auto_20150324_2240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pinnedtopic',
            name='topic',
        ),
        migrations.DeleteModel(
            name='PinnedTopic',
        ),
        migrations.AddField(
            model_name='topic',
            name='is_pinned',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
