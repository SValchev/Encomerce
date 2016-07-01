# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('status', models.CharField(max_length=225)),
                ('time_added', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to='payments.User')),
            ],
        ),
    ]
