# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20150228_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='last_post',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='last_post',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
