# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vnoiusers', '0002_auto_20150316_0213'),
    ]

    operations = [
        migrations.AddField(
            model_name='vnoiuser',
            name='contribution',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
