# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UnpadaidUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('email', models.CharField(unique=True, max_length=225)),
                ('last_notification', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('name', models.CharField(max_length=225)),
                ('email', models.EmailField(unique=True, max_length=225)),
                ('last_4_digits', models.CharField(null=True, blank=True, max_length=4)),
                ('stripe_id', models.CharField(max_length=225)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rank', models.CharField(default='Scary Noob', max_length=225)),
                ('fraction', models.CharField(max_length=225)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
