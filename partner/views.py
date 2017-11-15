# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from material.frontend.views import ModelViewSet, ListModelView

from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from . import models
from django.db.models import When, Q, F
from django.views import generic


class DistributorViewSet(ModelViewSet):
    model = models.Distributor


class ProductViewSet(ModelViewSet):
    model = models.Product

    def get_queryset(self, request):
        distributor = models.Distributor.objects.filter(user=request.user)
        return models.Product.objects.filter(distributor=distributor)

    list_display = ('code', 'name', 'packing', 'price', 'offer_id', 'active')


class OrderViewSet(ModelViewSet):
    model = models.Order

    def get_queryset(self, request):
        distributor = models.Distributor.objects.filter(user=request.user)
        retailer = models.Retailer.objects.filter(user=request.user)

        return models.Order.objects.filter(distributor=distributor) | models.Order.objects.filter(retailer=retailer)

    list_display = ('order_date', 'retailer', 'order_status', 'bill_total')

    def get_detail_view(self):
        return OrderItemView.as_view()


class OrderItemViewSet(ModelViewSet):
    model = models.OrderItem
    list_display = ('order', 'product', 'item_quantity')

    def get_queryset(self, request):
        distributor = models.Distributor.objects.filter(user=request.user)
        retailer = models.Retailer.objects.filter(user=request.user)
        order = models.Order.objects.filter(distributor=distributor) | models.Order.objects.filter(retailer=retailer)

        return models.OrderItem.objects.filter(order=order)


class OrderItemView(ListModelView):
    model = models.OrderItem
    template_name = 'partner/order_detail.html'
    list_display = ('order', 'product', 'item_quantity')

    def get_queryset(self):
        order_id = self.kwargs['pk']        
        return models.OrderItem.objects.filter(order_id__in=order_id)


class RetailerViewSet(ModelViewSet):
    model = models.Retailer

    list_display = ('store_name', 'store_number', 'store_address', 'user')

    def get_queryset(self, request):
        distributor = models.Distributor.objects.filter(user=request.user)
        retailers = models.ConnectedRetailer.objects.filter(distributor=distributor)
        return models.Retailer.objects.filter(distributor=distributor)

    def get_detail_view(self):
        return ConnectedRetailerView.as_view()


class RetailerView(ModelViewSet):
    model = models.Retailer
    list_display = ('store_name', 'store_number', 'store_address', 'user')


class ConnectedRetailerViewSet(ModelViewSet):
    model = models.ConnectedRetailer

    list_display = ('retailer', 'remaining')

    def get_queryset(self, request):
        distributor = models.Distributor.objects.filter(user=request.user)
        retailer = models.Retailer.objects.filter(user=request.user)

        return models.ConnectedRetailer.objects.filter(
            distributor=distributor) | models.ConnectedRetailer.objects.filter(retailer=retailer)


class ConnectedRetailerView(ListModelView):
    model = models.ConnectedRetailer
    list_display = ('retailer', 'remaining')

    def get_queryset(self):
        retailer_id = self.kwargs['pk']
        return models.ConnectedRetailer.objects.filter(retailer__user_id=retailer_id)
