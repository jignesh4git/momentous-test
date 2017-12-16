# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-16 12:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('partner', '0002_auto_20171216_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('mobile_no', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128)),
                ('permissions', models.CharField(blank=True, choices=[('sell_product', 'Sell Product'), ('add_product', 'Add Product'), ('add_partner', 'Add Partner')], max_length=255)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Partner')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
