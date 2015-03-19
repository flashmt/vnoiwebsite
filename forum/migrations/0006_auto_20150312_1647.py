# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import precise_bbcode.fields


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
            field=precise_bbcode.fields.BBCodeTextField(no_rendered_field=True),
            preserve_default=True,
        ),
    ]
