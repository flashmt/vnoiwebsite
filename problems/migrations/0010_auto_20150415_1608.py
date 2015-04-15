# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0009_auto_20150415_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spojproblemsubmission',
            name='verdict',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
