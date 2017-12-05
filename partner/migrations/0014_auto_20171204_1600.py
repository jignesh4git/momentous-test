# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-04 10:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0013_auto_20171204_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='retailer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='retailer', to='partner.Retailer'),
        ),
    ]