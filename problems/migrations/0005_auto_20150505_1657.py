# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0004_auto_20150505_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spojproblemsubmission',
            name='submission_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spojproblemsubmission',
            name='submission_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spojproblemsubmission',
            name='submission_language',
            field=models.ForeignKey(related_name='+', blank=True, to='problems.SpojProblemLanguage', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spojproblemsubmission',
            name='submission_memory',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spojproblemsubmission',
            name='submission_rank',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spojproblemsubmission',
            name='submission_status',
            field=models.IntegerField(default=15, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spojproblemsubmission',
            name='submission_time',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spojproblemsubmission',
            name='submission_verdict',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
