# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from material.frontend.views import ModelViewSet, ListModelView
from material import *
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from . import models
from django.db.models import When, Q, F
from django.views import generic
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse, QueryDict

class ConnectedPartnerViewSet(ModelViewSet):
    model = models.ConnectedPartner
    list_display = ('partner', 'connected_partner', 'credit_limit', 'remaining')

    def get_queryset(self, request):
        partner = models.Partner.objects.filter(user=request.user)
        emp = models.Employee.objects.filter(user=request.user).values('partner')
        if emp:
            partner = emp
        if not request.user.is_superuser:
           # partner = models.Partner.objects.filter(user=request.user)
             return models.ConnectedPartner.objects.filter(partner=partner) | models.ConnectedPartner.objects.filter(connected_partner__in=partner)
        return models.ConnectedPartner.objects.all()


class ProductViewSet(ModelViewSet):
    model = models.Product
    list_display = ('partner', 'connected_partner', 'base', 'selling_price', 'is_active')

    def get_queryset(self, request):
        emp = models.Employee.objects.filter(user=request.user).values('partner')
        if not request.user.is_superuser:
            partner = models.Partner.objects.filter(user=request.user)
            if emp:
                partner = emp
            return models.Product.objects.filter(partner=partner) | models.Product.objects.filter(connected_partner=partner)
        return models.Product.objects.all()

class ProductListView(ListView):
    model = models.Product

class OrderViewSet(ModelViewSet):
    model = models.Order
    list_display = (
        'connected_partner', 'order_date', 'invoice_id', 'order_status', 'delivery_date', 'requested_delivery_time',
        'bill_total')

    def get_queryset(self, request):
        emp = models.Employee.objects.filter(user=request.user).values('partner')
        if not request.user.is_superuser:
            partner = models.Partner.objects.filter(user=request.user)
            if emp:
                partner = emp
            return models.Order.objects.filter(partner=partner)  | models.Order.objects.filter(connected_partner=partner)
        return models.Order.objects.all()

    def get_detail_view(request):
        return OrderItemView.as_view()


class OrderInvoiceView(TemplateView, ListModelView):
    model = models.Order
    template_name = 'partner/invoices.html'

    def get(self, request, **kwargs):
        context = super(OrderInvoiceView, self).get_context_data(**kwargs)
        emp = models.Employee.objects.filter(user=request.user).values('partner')
        if not request.user.is_superuser:
            partner = models.Partner.objects.filter(user=request.user)
            if emp:
                partner = emp
            order = models.Order.objects.filter(partner=partner) | models.Order.objects.filter(connected_partner=partner)
            context['orders'] = order
        return render(
            request,
            'partner/invoices.html',
            context,
        )


class InvoiceDetailView(TemplateView, ListModelView):
    model = models.Order
    template_name = 'partner/invoice_detail.html'

    def get(self, request, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        order_id = self.kwargs['pk']
        partner_id = models.Order.objects.filter(id=order_id).values('partner')

        # get all context for invoice:
        context['order'] = models.Order.objects.filter(id=order_id)
        context['manufacturer'] = models.Partner.objects.filter(Q(id=partner_id) & Q(type='manufacturer'))
        context['distributor'] = models.Partner.objects.filter(Q(id=partner_id) & Q(type='distributor'))
        if not context['distributor']:
            context['distributor'] = context['manufacturer']
        context['retailer'] = models.Partner.objects.filter(Q(id=partner_id) & Q(type='retailer'))
        context['orderitems'] = models.OrderItem.objects.filter(order_id=order_id)
        orderproducts = models.Product.objects.in_bulk(context['orderitems'])
        context['orderproducts'] = [orderproducts[orderproduct] for orderproduct in orderproducts]
        return render(
            request,
            'partner/invoice_detail.html',
            context,
        )


class OrderItemViewSet(ModelViewSet):
    model = models.OrderItem
    list_display = ('order_id', 'product', 'item_quantity')

    def get_queryset(self, request):
        emp = models.Employee.objects.filter(user=request.user).values('partner')
        if not request.user.is_superuser:
            partner = models.Partner.objects.filter(user=request.user)
            if emp:
                partner = emp
            order = models.Order.objects.filter(partner=partner)
            return models.OrderItem.objects.filter(order__in=order)
        return models.OrderItem.objects.all()


class OrderItemView(ListModelView):
    model = models.OrderItem
    list_display = ('order_id', 'product', 'item_quantity')

    def get_queryset(self):
        order_id = self.kwargs['pk']
        # invoice_id = models.Order.objects.filter(id=order_id)
        return models.OrderItem.objects.filter(order_id=order_id)
