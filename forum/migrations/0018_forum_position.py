# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0017_forumgroup_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='position',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
