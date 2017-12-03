# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-14 09:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectedRetailer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_limit', models.IntegerField()),
                ('remaining', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Distributer',
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
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(auto_created=True)),
                ('order_status', models.CharField(max_length=255)),
                ('item_total', models.CharField(blank=True, max_length=255)),
                ('s_gst', models.CharField(blank=True, max_length=255)),
                ('c_gst', models.CharField(blank=True, max_length=255)),
                ('other_charge_description', models.CharField(blank=True, max_length=255)),
                ('other_charge', models.CharField(blank=True, max_length=255)),
                ('bill_total', models.CharField(blank=True, max_length=255)),
                ('distributer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Distributer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Order')),
            ],
        ),
        migrations.CreateModel(
            name='partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('packing', models.CharField(max_length=255)),
                ('price', models.CharField(blank=True, max_length=255)),
                ('offer_id', models.CharField(blank=True, max_length=255)),
                ('active', models.BooleanField()),
                ('category', models.CharField(blank=True, max_length=255)),
                ('HSN', models.CharField(blank=True, max_length=255)),
                ('distributer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Distributer')),
            ],
        ),
        migrations.CreateModel(
            name='Retailer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=255)),
                ('store_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128)),
                ('store_address', models.CharField(max_length=255)),
                ('pin_code', models.CharField(max_length=255)),
                ('GSTIN', models.CharField(blank=True, max_length=255)),
                ('PAN', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='retailer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Retailer'),
        ),
        migrations.AddField(
            model_name='connectedretailer',
            name='distributer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Distributer'),
        ),
        migrations.AddField(
            model_name='connectedretailer',
            name='retailer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Retailer'),
        ),
    ]
