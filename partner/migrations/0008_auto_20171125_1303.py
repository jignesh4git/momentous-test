# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-25 07:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0007_product_final_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='c_gst',
            field=models.IntegerField(choices=[(0, '0'), (5, '5'), (12, '12'), (18, '18'), (28, '28')], default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='s_gst',
            field=models.IntegerField(choices=[(0, '0'), (5, '5'), (12, '12'), (18, '18'), (28, '28')], default=0),
        ),
    ]
