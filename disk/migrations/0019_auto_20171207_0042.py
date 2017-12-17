# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-07 00:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('disk', '0018_auto_20171207_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='aliconfig',
            name='AppName',
            field=models.CharField(blank=True, default=None, max_length=20, null=True, verbose_name='APP广告位名称'),
        ),
        migrations.AddField(
            model_name='aliconfig',
            name='AppPid',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AppId', to='disk.Agent', verbose_name='APP广告位'),
        ),
        migrations.AddField(
            model_name='aliconfig',
            name='ZhaohuoName',
            field=models.CharField(blank=True, default=None, max_length=20, null=True, verbose_name='找货广告名称'),
        ),
        migrations.AddField(
            model_name='aliconfig',
            name='ZhaohuoPid',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ZhId', to='disk.Agent', verbose_name='找货广告位'),
        ),
    ]