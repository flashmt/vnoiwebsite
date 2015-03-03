# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0001_squashed_0008_auto_20150301_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'u', max_length=5, choices=[(b'u', b'UpVote'), (b'd', b'DownVote')])),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(related_name='votes', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(related_name='votes', to='forum.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='post',
            old_name='num_votes',
            new_name='num_downvotes',
        ),
        migrations.AddField(
            model_name='post',
            name='num_upvotes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
