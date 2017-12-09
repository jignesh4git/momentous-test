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

class ConnectedPartnerViewSet(ModelViewSet):
    model = models.ConnectedPartner
    list_display = ('partner', 'connected_partner', 'credit_limit', 'remaining')


class ProductViewSet(ModelViewSet):
    model = models.Product
    list_display = ('partner', 'product_partner', 'base', 'selling_price', 'is_active')

    def get_queryset(self, request):
        partner = models.Partner.objects.filter(user=request.user)
        return models.Product.objects.filter(partner=partner) | models.Product.objects.filter(product_partner=partner)

class OrderViewSet(ModelViewSet):
    model = models.Order
    list_display = (
    'order_partner', 'order_date', 'invoice_id', 'order_status', 'delivery_date', 'requested_delivery_time',
    'bill_total')

    def get_queryset(self, request):
        partner = models.Partner.objects.filter(user=request.user)
        return models.Order.objects.filter(partner=partner)

    def get_detail_view(request):
        return OrderDetailView.as_view()


class OrderInvoiceView(TemplateView, ListModelView):
    model = models.OrderItem
    list_display = ('order', 'product', 'item_quantity')
    template_name = 'partner/invoices.html'

    def get(self, request, **kwargs):
        context = super(OrderInvoiceView, self).get_context_data(**kwargs)
        partner = models.Partner.objects.filter(user=request.user)
        order = models.Order.objects.filter(partner=partner) | models.Order.objects.filter(order_partner=partner)
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
        partner_id = models.Order.objects.filter(id=order_id).values('partner')

        # get all context for invoice:
        context['order'] = models.Order.objects.filter(id=order_id)
        context['manufacturer'] = models.Partner.objects.filter(Q(id=partner_id) | Q(type='manufacturer'))
        context['distributor'] = models.Partner.objects.filter(Q(id=partner_id) & Q(type='distributor'))
        context['retailer'] = models.Partner.objects.filter(id=partner_id) | models.Partner.objects.filter(type='retailer')
        context['orderitems'] = models.OrderItem.objects.filter(order_id=order_id)
        orderproducts = models.Product.objects.in_bulk(context['orderitems'])
        context['orderproducts'] = [orderproducts[orderproduct] for orderproduct in orderproducts]

        return context


class OrderItemViewSet(ModelViewSet):
    model = models.OrderItem

    def get_queryset(self, request):
        if not request.user.is_superuser:
            partner = models.Partner.objects.filter(user=request.user)
            order = models.Order.objects.filter(partner=partner)
            return models.OrderItem.objects.filter(order__in=order)
        return models.OrderItem.objects.all()

    def get_detail_view(request):
        return OrderItemView.as_view()


class OrderItemView(ListModelView):
    model = models.OrderItem
    list_display = ('order', 'product', 'item_quantity')

    def get_queryset(self):
        order_id = self.kwargs['pk']
        # invoice_id = models.Order.objects.filter(id=order_id)
        return models.OrderItem.objects.filter(order_id=order_id)
