# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_auto_20150319_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='pinnedtopic',
            name='created_at',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
