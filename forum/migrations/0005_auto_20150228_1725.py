# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20150228_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='last_post',
            field=models.OneToOneField(related_name='+', null=True, default=None, blank=True, to='forum.Post'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='last_post',
            field=models.OneToOneField(related_name='+', null=True, default=None, blank=True, to='forum.Post'),
            preserve_default=True,
        ),
    ]
