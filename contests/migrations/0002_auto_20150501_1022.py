# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NonStandardContestForum',
            new_name='ContestForum',
        ),
        migrations.RenameModel(
            old_name='NonStandardContestStandingTable',
            new_name='ContestStandingTable',
        ),
    ]
