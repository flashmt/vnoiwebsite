# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20150312_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='_content_rendered',
        ),
        migrations.AlterField(
            model_name='topic',
            name='content',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
