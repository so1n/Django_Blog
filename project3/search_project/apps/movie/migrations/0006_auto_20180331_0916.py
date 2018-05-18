# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-31 09:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0005_auto_20180331_0251'),
    ]

    operations = [
        migrations.CreateModel(
            name='RMovieTicketInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_type', models.CharField(default='', max_length=50, verbose_name='类型')),
                ('ticket_url', models.CharField(default='', max_length=200, verbose_name='url')),
                ('ticket_s_time', models.CharField(default='', max_length=50, verbose_name='开始时间')),
                ('ticket_e_time', models.CharField(default='', max_length=50, verbose_name='结束时间')),
                ('ticket_lg', models.CharField(default='', max_length=50, verbose_name='语言')),
                ('ticket_tn', models.CharField(default='', max_length=50, verbose_name='厅')),
                ('ticket_np', models.CharField(default='', max_length=50, verbose_name='新价格')),
                ('ticket_op', models.CharField(default='', max_length=50, verbose_name='旧价格')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '电影票信息',
                'verbose_name_plural': '电影票信息',
            },
        ),
        migrations.AddField(
            model_name='movieticketinfo',
            name='ticket_cinema',
            field=models.CharField(default='', max_length=50, verbose_name='影院'),
        ),
        migrations.AddField(
            model_name='movieticketinfo',
            name='ticket_type',
            field=models.CharField(default='', max_length=50, verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='movieticketinfo',
            name='ticket_movie',
            field=models.CharField(default='', max_length=50, verbose_name='电影名'),
        ),
    ]