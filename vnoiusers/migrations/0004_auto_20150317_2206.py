# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vnoiusers', '0003_vnoiuser_contribution'),
    ]

    operations = [
        migrations.AddField(
            model_name='vnoiuser',
            name='codeforces_account',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vnoiuser',
            name='topcoder_account',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vnoiuser',
            name='voj_account',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
