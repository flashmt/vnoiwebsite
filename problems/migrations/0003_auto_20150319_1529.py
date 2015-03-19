# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0002_auto_20150313_1837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spojproblem',
            name='_statement_rendered',
        ),
        migrations.AlterField(
            model_name='spojproblem',
            name='statement',
            field=django_bleach.models.BleachField(null=True),
            preserve_default=True,
        ),
    ]
