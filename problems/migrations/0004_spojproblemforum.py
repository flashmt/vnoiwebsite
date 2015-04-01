# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0015_auto_20150327_1216'),
        ('problems', '0003_auto_20150319_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpojProblemForum',
            fields=[
                ('forum_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='forum.Forum')),
                ('problem', models.ForeignKey(related_name='forum', to='problems.SpojProblem')),
            ],
            options={
            },
            bases=('forum.forum',),
        ),
    ]
