# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('avatar', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VnoiUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40, blank=True)),
                ('dob', models.DateField(null=True, blank=True)),
                ('contribution', models.IntegerField(default=0)),
                ('voj_account', models.CharField(max_length=100, null=True, blank=True)),
                ('voj_password', models.CharField(max_length=100, null=True, blank=True)),
                ('codeforces_account', models.CharField(max_length=100, null=True, blank=True)),
                ('topcoder_account', models.CharField(max_length=100, null=True, blank=True)),
                ('topcoder_account_url', models.CharField(max_length=1024, null=True, blank=True)),
                ('avatar', models.OneToOneField(related_name='vnoiuser', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='avatar.Avatar')),
                ('friends', models.ManyToManyField(related_name='+', null=True, to='vnoiusers.VnoiUser', blank=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
