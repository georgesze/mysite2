# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-20 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disk', '0003_auto_20170720_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alimama',
            name='id',
        ),
        migrations.AddField(
            model_name='alimama',
            name='order',
            field=models.CharField(default='', max_length=20, primary_key=True, serialize=False, verbose_name='订单编号'),
        ),
    ]
