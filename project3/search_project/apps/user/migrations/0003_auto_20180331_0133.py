# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-31 01:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_usertag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertag',
            name='user',
            field=models.CharField(default='', max_length=50, verbose_name='用户'),
        ),
    ]
