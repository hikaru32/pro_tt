# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-05 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usercenter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ttsxuser',
            name='uaddress',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='ttsxuser',
            name='ucode',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AlterField(
            model_name='ttsxuser',
            name='uphone',
            field=models.CharField(blank=True, max_length=11),
        ),
        migrations.AlterField(
            model_name='ttsxuser',
            name='ushou',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]