# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-13 15:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car_workshop', '0006_task_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carmodel',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='job',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='task',
            name='slug',
        ),
    ]
