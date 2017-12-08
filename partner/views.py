# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from material.frontend.views import ModelViewSet, ListModelView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from . import models
from django.db.models import When, Q, F
from django.views import generic
from django.views.generic import TemplateView

class DistributorViewSet(ModelViewSet):
    model = models.Distributor


class ProductViewSet(ModelViewSet):
    model = models.Product
    list_display = ('code', 'name', 'packing', 'price', 's_gst', 'c_gst', 'final_price', 'offer_id', 'active')

    def get_queryset(self, request):
        manufacturer = models.Manufacturer.objects.filter(user=request.user)
        distributor = models.Distributor.objects.filter(user=request.user)
        retailer = models.Retailer.objects.filter(user=request.user)
        if retailer:
            distributor = models.ConnectedRetailer.objects.filter(retailer=retailer).values('distributor')
        return models.Product.objects.filter(manufacturer__in=manufacturer) | models.Product.objects.filter(distributor__in=distributor)


class OrderViewSet(ModelViewSet):
    model = models.Order
    list_display = ('order_date', 'invoice_id', 'retailer', 'order_status', 'bill_total')

    def get_queryset(self, request):
        manufacturer = models.Manufacturer.objects.filter(user=request.user)
        distributor = models.Distributor.objects.filter(user=request.user)
        retailer = models.Retailer.objects.filter(user=request.user)
        return models.Order.objects.filter(manufacturer=manufacturer) | models.Order.objects.filter(distributor=distributor) | models.Order.objects.filter(retailer=retailer)

    def get_detail_view(request):
        return OrderDetailView.as_view()


class OrderInvoiceView(TemplateView, ListModelView):
    model = models.OrderItem
    list_display = ('order', 'product', 'item_quantity')
    template_name = 'partner/invoices.html'

    def get(self, request, **kwargs):
        context = super(OrderInvoiceView, self).get_context_data(**kwargs)
        manufacturer = models.Manufacturer.objects.filter(user=request.user)
        distributor = models.Distributor.objects.filter(user=request.user)
        retailer = models.Retailer.objects.filter(user=request.user)
        order = models.Order.objects.filter(manufacturer = manufacturer) | models.Order.objects.filter(distributor=distributor) | models.Order.objects.filter(retailer=retailer)
        order_id = models.OrderItem.objects.filter(order__in=order).order_by('retailer')
        context['orders'] = order
        return render(
            request,
            'partner/invoices.html',
            context,
        )


class OrderDetailView(TemplateView, ListModelView):
    model = models.Order
    template_name = 'partner/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        order_id = self.kwargs['pk']
        dist_id = models.Order.objects.filter(id=order_id).values('distributor_id')
        ret_id = models.Order.objects.filter(id=order_id).values('retailer_id')

        # get all context for invoice:
        context['order'] = models.Order.objects.filter(id=order_id)
        context['distributor'] = models.Distributor.objects.filter(id__in=dist_id)
        context['retailer'] = models.Retailer.objects.filter(id__in=ret_id)
        context['orderitems'] = models.OrderItem.objects.filter(order_id=order_id)
        orderproducts = models.Product.objects.in_bulk(context['orderitems'])
        context['orderproducts'] = [orderproducts[orderproduct] for orderproduct in orderproducts]

        return context


class OrderItemViewSet(ModelViewSet):
    model = models.OrderItem

    def get_queryset(self, request):
        manufacturer = models.Manufacturer.objects.filter(user=request.user)
        distributor = models.Distributor.objects.filter(user=request.user)
        retailer = models.Retailer.objects.filter(user=request.user)
        order = models.Order.objects.filter(manufacturer = manufacturer) | models.Order.objects.filter(distributor=distributor) | models.Order.objects.filter(retailer=retailer)
        return models.OrderItem.objects.filter(order__in=order)

    def get_detail_view(request):
        return OrderItemView.as_view()


class OrderItemView(ListModelView):
    model = models.OrderItem
    list_display = ('order', 'product', 'item_quantity')

    def get_queryset(self):
        order_id = self.kwargs['pk']
        # invoice_id = models.Order.objects.filter(id=order_id)
        return models.OrderItem.objects.filter(order_id=order_id)


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
