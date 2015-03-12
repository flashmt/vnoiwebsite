# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20150303_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='PinnedTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', models.ForeignKey(related_name='topics', to='forum.Topic')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
