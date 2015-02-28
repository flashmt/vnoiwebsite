# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20150228_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='last_post',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='last_post',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
    ]
