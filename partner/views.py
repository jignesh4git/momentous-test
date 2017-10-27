# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from material.frontend.views import ModelViewSet, ListModelView

from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from . import models


class DistributerViewSet(ModelViewSet):
    model = models.Distributer


class ProductViewSet(ModelViewSet):
    model = models.Product

    def get_queryset(self, request):
        distributer = models.Distributer.objects.filter(user=request.user)
        return models.Product.objects.filter(distributer=distributer)

    list_display = ('code', 'name', 'packing', 'price', 'offer_id', 'active')


class OrderViewSet(ModelViewSet):
    model = models.Order

    def get_queryset(self, request):
        distributer = models.Distributer.objects.filter(user=request.user)
        retailer = models.Retailer.objects.filter(user=request.user)
        return models.Order.objects.filter(distributer=distributer) | models.Order.objects.filter(retailer=retailer)

    list_display = ('order_date', 'retailer', 'order_status', 'bill_total')

    def get_detail_view(self):
        return OrderDetailView.as_view()


class RetailerViewSet(ModelViewSet):
    model = models.Retailer

    list_display = ('store_name', 'store_number', 'store_address', 'user')

    def get_queryset(self, request):
        distributer = models.Distributer.objects.filter(user=request.user)
        connected_retailers = models.ConnectedRetailer.objects.filter(distributer=distributer)
        return models.Retailer.objects.filter(user__in=list(connected_retailers.values('retailer')))


class OrderDetailView(ListModelView):
    model = models.Order
    template_name = 'partner/order_detail.html'

    list_display = ('product', 'item_quantity')

# @login_required
# def update_profile(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, _('Your profile was successfully updated!'))
#             return redirect('settings:profile')
#         else:
#             messages.error(request, _('Please correct the error below.'))
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'profiles/profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })
