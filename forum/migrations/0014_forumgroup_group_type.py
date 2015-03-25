# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0013_auto_20150324_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumgroup',
            name='group_type',
            field=models.CharField(default=b'f', max_length=3, choices=[(b'f', b'Forum'), (b'l', b'Library')]),
            preserve_default=True,
        ),
    ]
