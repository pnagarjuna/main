# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-04 11:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regform', '0004_usertable_middle_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertable',
            name='middle_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='middle_name'),
        ),
    ]
