# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-12 15:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0002_auto_20171212_2029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='partner',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
    ]
