# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vnoiusers', '0005_vnoiuser_topcoder_account_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='vnoiuser',
            name='friends',
            field=models.ManyToManyField(related_name='+', to='vnoiusers.VnoiUser'),
            preserve_default=True,
        ),
    ]
