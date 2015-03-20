# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='_content_rendered',
            field=models.TextField(null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='content',
            field=models.TextField(null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
