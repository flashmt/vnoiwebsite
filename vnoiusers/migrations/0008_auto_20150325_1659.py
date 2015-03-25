# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vnoiusers', '0007_vnoiuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vnoiuser',
            name='dob',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
