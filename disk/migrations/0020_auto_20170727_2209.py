# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-27 14:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('disk', '0019_auto_20170727_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliconfig',
            name='AgentId',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AId', to='disk.Agent'),
        ),
        migrations.AlterField(
            model_name='aliconfig',
            name='AgentUpId',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AUpId', to='disk.Agent'),
        ),
    ]
