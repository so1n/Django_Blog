# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-06 22:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usermessage',
            options={'verbose_name': '用户消息', 'verbose_name_plural': '用户消息'},
        ),
    ]