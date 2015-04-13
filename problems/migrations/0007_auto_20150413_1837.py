# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0006_auto_20150413_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spojproblemlanguage',
            name='name',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
