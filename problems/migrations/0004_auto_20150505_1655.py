# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0003_auto_20150505_1105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spojproblemsubmission',
            old_name='submission_data',
            new_name='submission_date',
        ),
        migrations.AddField(
            model_name='spojproblemsubmission',
            name='submission_status',
            field=models.IntegerField(default=15),
            preserve_default=True,
        ),
    ]
