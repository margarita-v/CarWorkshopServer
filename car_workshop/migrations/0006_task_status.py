# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-10 14:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_workshop', '0005_auto_20170708_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
