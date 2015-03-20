# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_auto_20150319_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='pinnedtopic',
            name='author',
            field=models.CharField(max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pinnedtopic',
            name='content',
            field=django_bleach.models.BleachField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pinnedtopic',
            name='forum_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pinnedtopic',
            name='is_cached',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pinnedtopic',
            name='topic_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pinnedtopic',
            name='topic_title',
            field=models.CharField(max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
    ]
