# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-06 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disk', '0006_auto_20170731_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliord',
            name='CommType',
            field=models.CharField(default='', max_length=40, verbose_name='商品信息'),
        ),
        migrations.AlterField(
            model_name='aliord',
            name='SettleDate',
            field=models.DateTimeField(default='', verbose_name='结算时间'),
        ),
    ]
