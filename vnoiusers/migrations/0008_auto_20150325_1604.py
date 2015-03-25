# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vnoiusers', '0007_vnoiuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='vnoiuser',
            name='activation_key',
            field=models.CharField(default=11111, max_length=40, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vnoiuser',
            name='friends',
            field=models.ManyToManyField(related_name='+', null=True, to='vnoiusers.VnoiUser', blank=True),
            preserve_default=True,
        ),
    ]
