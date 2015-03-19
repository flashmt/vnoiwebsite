# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vnoiusers', '0004_auto_20150317_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='vnoiuser',
            name='topcoder_account_url',
            field=models.CharField(max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
    ]
