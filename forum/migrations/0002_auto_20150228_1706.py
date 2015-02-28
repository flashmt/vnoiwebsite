# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='last_post',
            field=models.OneToOneField(related_name='+', default=None, to='forum.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_posts', default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='last_post',
            field=models.OneToOneField(related_name='+', default=None, to='forum.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_topics', default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
