# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-14 03:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disk', '0009_auto_20170811_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='aliconfig',
            name='CalculateStatus',
            field=models.CharField(blank=True, default='', max_length=10, verbose_name='计算状态'),
        ),
        migrations.AddField(
            model_name='aliconfig',
            name='IncomeLv1',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='下级贡献佣金'),
        ),
        migrations.AddField(
            model_name='aliconfig',
            name='IncomeLv2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='二级贡献佣金'),
        ),
        migrations.AddField(
            model_name='aliconfig',
            name='IncomeSelf',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='自获佣金额'),
        ),
        migrations.AddField(
            model_name='aliconfig',
            name='IncomeTotal',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='总佣金'),
        ),
    ]
