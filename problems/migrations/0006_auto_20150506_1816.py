# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0005_auto_20150505_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpojUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='spojproblemsubmission',
            name='voj_account',
            field=models.ForeignKey(related_name='submissions', blank=True, to='problems.SpojUser', null=True),
            preserve_default=True,
        ),
    ]
