# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0002_spojproblemlanguage_fullname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spojproblemsubmission',
            name='submission_language',
            field=models.ForeignKey(related_name='+', to='problems.SpojProblemLanguage'),
            preserve_default=True,
        ),
    ]
