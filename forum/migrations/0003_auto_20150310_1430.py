# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20150303_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='last_post',
            field=models.OneToOneField(related_name='+', null=True, on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='forum.Post'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='created_by',
            field=models.ForeignKey(related_name='created_posts', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='reply_on',
            field=models.ForeignKey(related_name='reply_posts', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='forum.Post', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(related_name='posts', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Topic', to='forum.Topic', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_posts', on_delete=django.db.models.deletion.SET_NULL, default=None, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='last_post',
            field=models.OneToOneField(related_name='+', null=True, on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='forum.Post'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_topics', on_delete=django.db.models.deletion.SET_NULL, default=None, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
