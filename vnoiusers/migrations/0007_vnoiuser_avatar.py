# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('avatar', '__first__'),
        ('vnoiusers', '0006_vnoiuser_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='vnoiuser',
            name='avatar',
            field=models.OneToOneField(related_name='vnoiuser', null=True, blank=True, to='avatar.Avatar'),
            preserve_default=True,
        ),
    ]
