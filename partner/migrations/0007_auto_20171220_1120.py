# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-20 05:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0006_remove_order_connected_partner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='selling_price',
            field=models.FloatField(null=True),
        ),
    ]