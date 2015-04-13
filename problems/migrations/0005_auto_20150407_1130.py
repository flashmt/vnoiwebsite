# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0004_spojproblemforum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spojproblem',
            name='allowed_language',
            field=models.CharField(default=b'', max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spojproblem',
            name='category',
            field=models.ForeignKey(related_name='problems', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='problems.SpojProblemCategory', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spojproblem',
            name='cluster',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='problems.SpojCluster', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spojproblemforum',
            name='problem',
            field=models.ForeignKey(related_name='forum', blank=True, to='problems.SpojProblem', null=True),
            preserve_default=True,
        ),
    ]
