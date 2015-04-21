# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0010_auto_20150415_1608'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spojproblemsubmission',
            old_name='row',
            new_name='participant',
        ),
    ]
