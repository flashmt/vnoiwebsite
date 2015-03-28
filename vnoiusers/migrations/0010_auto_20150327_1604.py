# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vnoiusers', '0009_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vnoiuser',
            name='avatar',
            field=models.OneToOneField(related_name='vnoiuser', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='avatar.Avatar'),
            preserve_default=True,
        ),
    ]
