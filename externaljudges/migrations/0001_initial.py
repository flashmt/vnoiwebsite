# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContestSchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('judge', models.CharField(max_length=2, choices=[(b'cf', b'Codeforces'), (b'tc', b'Topcoder')])),
                ('contest_name', models.CharField(max_length=255)),
                ('start_time', models.DateTimeField()),
                ('duration', models.IntegerField(default=120)),
                ('url', models.CharField(max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
