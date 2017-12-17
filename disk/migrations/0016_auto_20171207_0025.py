# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-07 00:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('disk', '0015_auto_20171207_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliconfig',
            name='AppName',
            field=models.CharField(blank=True, default=None, max_length=20, null=True, verbose_name='APP广告位名称'),
        ),
        migrations.AlterField(
            model_name='aliconfig',
            name='AppPid',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AppId', to='disk.Agent', verbose_name='APP广告位'),
        ),
    ]