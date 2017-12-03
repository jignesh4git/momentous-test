# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-03 17:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0010_auto_20171203_2306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manufacturer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='connecteddistributor',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='distributor',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='product',
            name='manufacturer',
        ),
        migrations.DeleteModel(
            name='Manufacturer',
        ),
    ]
