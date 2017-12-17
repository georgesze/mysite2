# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-15 01:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('disk', '0021_auto_20171211_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliconfig',
            name='AgentId',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AId', to='disk.Agent', verbose_name='代理'),
        ),
    ]