# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_workshop', '0010_auto_20171022_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='number',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='task',
            name='vin',
            field=models.CharField(max_length=17),
        ),
    ]
