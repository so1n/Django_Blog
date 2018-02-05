# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-05 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180204_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], default='男', max_length=6, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号码'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_image',
            field=models.ImageField(default='image/default.png', upload_to='image/%y/%m', verbose_name='用户头像'),
        ),
    ]
