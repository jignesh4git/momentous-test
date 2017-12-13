# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.views import generic

from . import views


urlpatterns = [
    url('^$', generic.TemplateView.as_view(template_name="partner/index.html"), name="index"),
    url('^invoices/', views.OrderInvoiceView.as_view(), name="orderinvoice_list"),
    url('^invoice/(?P<pk>[0-9]+)/detail/', views.InvoiceDetailView.as_view(),name="invoicedetail"),
    url('^order/', include(views.OrderViewSet().urls), name="order_list"),
    url('^product/', include(views.ProductViewSet().urls), name="product_list"),
    url('^orderitem/', include(views.OrderItemViewSet().urls), name="orderitem_list"),
    url('^connectedpartner/', include(views.ConnectedPartnerViewSet().urls), name="connectedpartner_list")
]