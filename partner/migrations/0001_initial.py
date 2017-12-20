# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-19 07:32
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
            name='BaseProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('packing', models.CharField(max_length=255)),
                ('s_gst', models.IntegerField(choices=[(0, '0'), (5, '5'), (12, '12'), (18, '18'), (28, '28')], default=0)),
                ('c_gst', models.IntegerField(choices=[(0, '0'), (5, '5'), (12, '12'), (18, '18'), (28, '28')], default=0)),
                ('category', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Product Master',
            },
        ),
        migrations.CreateModel(
            name='ConnectedDistributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_limit', models.IntegerField()),
                ('remaining', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ConnectedPartner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_limit', models.IntegerField()),
                ('remaining', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ConnectedRetailer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_limit', models.IntegerField()),
                ('remaining', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Distributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('company_name', models.CharField(max_length=255)),
                ('company_address', models.CharField(max_length=255)),
                ('pin_code', models.CharField(max_length=255)),
                ('GSTIN', models.CharField(blank=True, max_length=255)),
                ('PAN', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('mobile_no', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128)),
                ('permissions', models.CharField(blank=True, choices=[('sell_product', 'Sell Product'), ('add_product', 'Add Product'), ('add_partner', 'Add Partner')], max_length=255)),
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
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(auto_created=True)),
                ('order_status', models.CharField(max_length=255)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('requested_delivery_time', models.DateField(blank=True, null=True)),
                ('item_total', models.CharField(blank=True, max_length=255, null=True)),
                ('s_gst_total', models.CharField(blank=True, max_length=255, null=True)),
                ('c_gst_total', models.CharField(blank=True, max_length=255, null=True)),
                ('other_charge_description', models.CharField(blank=True, max_length=255)),
                ('other_charge', models.CharField(blank=True, max_length=255, null=True)),
                ('bill_total', models.CharField(blank=True, max_length=255)),
                ('invoice_id', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['-order_date'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_quantity', models.IntegerField()),
                ('total', models.IntegerField(blank=True)),
                ('s_gst', models.CharField(blank=True, max_length=255)),
                ('c_gst', models.CharField(blank=True, max_length=255)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Order')),
            ],
            options={
                'verbose_name_plural': 'Invoices',
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('alternate_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('company_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('pin_code', models.CharField(max_length=255)),
                ('GSTIN', models.CharField(blank=True, max_length=255)),
                ('PAN', models.CharField(blank=True, max_length=255)),
                ('ADHAAR', models.CharField(blank=True, max_length=255)),
                ('type', models.CharField(choices=[('manufacturer', 'Manufacturer'), ('distributor', 'Distributor'), ('retailer', 'Retailer')], max_length=255)),
                ('permissions', models.CharField(blank=True, choices=[('sell_product', 'Sell Product'), ('add_product', 'Add Product'), ('add_partner', 'Add Partner')], max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selling_price', models.FloatField()),
                ('is_active', models.BooleanField()),
                ('base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.BaseProduct')),
                ('connected_partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_partner', to='partner.Partner')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Partner')),
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
                ('distributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Distributor')),
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
            name='connected_partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_partner', to='partner.Partner'),
        ),
        migrations.AddField(
            model_name='order',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Partner'),
        ),
        migrations.AddField(
            model_name='employee',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Partner'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='distributor',
            name='manufacturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='partner.Manufacturer'),
        ),
        migrations.AddField(
            model_name='distributor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='connectedretailer',
            name='distributor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Distributor'),
        ),
        migrations.AddField(
            model_name='connectedretailer',
            name='retailer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Retailer'),
        ),
        migrations.AddField(
            model_name='connectedpartner',
            name='connected_partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connected_partner', to='partner.Partner'),
        ),
        migrations.AddField(
            model_name='connectedpartner',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partner', to='partner.Partner'),
        ),
        migrations.AddField(
            model_name='connecteddistributor',
            name='distributor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Distributor'),
        ),
        migrations.AddField(
            model_name='connecteddistributor',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Manufacturer'),
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Partner'),
        ),
    ]
