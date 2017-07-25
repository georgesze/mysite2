# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-21 08:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disk', '0010_auto_20170721_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliord',
            name='AllowanceAmt',
            field=models.CharField(default='', max_length=8, verbose_name='补贴金额'),
        ),
        migrations.AlterField(
            model_name='aliord',
            name='AllowancePerc',
            field=models.CharField(default='', max_length=8, verbose_name='补贴比例'),
        ),
        migrations.AlterField(
            model_name='aliord',
            name='DividePerc',
            field=models.CharField(default='', max_length=8, verbose_name='分成比率'),
        ),
        migrations.AlterField(
            model_name='aliord',
            name='IncomePerc',
            field=models.CharField(default='', max_length=8, verbose_name='收入比率'),
        ),
        migrations.AlterField(
            model_name='aliord',
            name='RebatePerc',
            field=models.CharField(default='', max_length=8, verbose_name='佣金比例'),
        ),
    ]
