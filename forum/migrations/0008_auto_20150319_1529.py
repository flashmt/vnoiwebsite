# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_auto_20150319_0254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=django_bleach.models.BleachField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='content',
            field=django_bleach.models.BleachField(),
            preserve_default=True,
        ),
    ]
