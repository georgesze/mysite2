# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-20 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disk', '0008_auto_20170720_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliord',
            name='ClickDate',
            field=models.DateTimeField(default='', verbose_name='点击时间'),
        ),
        migrations.AlterField(
            model_name='aliord',
            name='CreatDate',
            field=models.DateTimeField(default='', verbose_name='创建时间'),
        ),
    ]
