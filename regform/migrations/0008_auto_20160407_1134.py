# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-07 06:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regform', '0007_auto_20160407_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertable',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
    ]
