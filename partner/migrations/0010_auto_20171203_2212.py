# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-03 16:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('partner', '0009_auto_20171203_1228'),
    ]
    operations = [
        migrations.CreateModel(
            name='ConnectedDistributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_limit', models.IntegerField()),
                ('remaining', models.IntegerField()),
                ('distributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Distributor')),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('company_name', models.CharField(max_length=255)),
                ('company_address', models.CharField(max_length=255)),
                ('pin_code', models.CharField(max_length=255)),
                ('GSTIN', models.CharField(blank=True, max_length=255)),
                ('PAN', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='connecteddistributor',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Manufacturer'),
        ),
        migrations.AddField(
            model_name='distributor',
            name='manufacturer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='partner.Manufacturer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='manufacturer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='manufacturer', to='partner.Manufacturer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='manufacturer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='partner.Manufacturer'),
            preserve_default=False,
        ),
    ]
