# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-19 07:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('partner', '0002_auto_20171219_1303'),
    ]
