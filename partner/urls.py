# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.views import generic

from . import views


urlpatterns = [
    url('^$', generic.TemplateView.as_view(template_name="partner/index.html"), name="index"),
    url('^invoices/', views.OrderInvoiceView.as_view(), name="orderinvoice_list"),
    url('^distributor/', include(views.DistributorViewSet().urls), name="distributor_list"),
    url('^retailer/', include(views.RetailerViewSet().urls), name="retailer_list"),
    url('^order/', include(views.OrderViewSet().urls), name="order_list"),
    url('^product/', include(views.ProductViewSet().urls), name="product_list"),
    url('^orderitem/', include(views.OrderItemViewSet().urls), name="orderitem_list"),
    url('^connectedretailer/', include(views.ConnectedRetailerViewSet().urls), name="connectedretailer_list")
]