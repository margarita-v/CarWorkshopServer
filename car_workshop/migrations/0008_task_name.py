# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-13 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_workshop', '0007_auto_20170713_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='name',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]
