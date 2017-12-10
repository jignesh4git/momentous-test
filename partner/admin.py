from django import forms
from django.contrib import admin
from . import models
from .models import Order
from django.contrib.auth.models import Group

# Register your models here.
class PartnerAdmin(admin.ModelAdmin):
    list_display=('company_name','mobile_number','address','GSTIN','PAN','ADHAAR')

     def get_queryset(self, request):
         partner = models.Partner.objects.filter(user=request.user)   
         if not request.user.is_superuser:
        #    partner = models.Partner.objects.filter(user=request.user)
         return models.Partner.objects.filter(id=partner)
         return models.Partner.objects.all()


class ConnectedPartnerAdmin(admin.ModelAdmin):
    list_display=('partner','connected_partner','credit_limit','remaining')

    def get_queryset(self, request):
        partner = models.Partner.objects.filter(user=request.user)
       # if not request.user.is_superuser:
           # partner = models.Partner.objects.filter(user=request.user)
        return models.ConnectedPartner.objects.filter(partner=partner) | models.ConnectedPartner.objects.filter(connected_partner__in=partner)
        return models.ConnectedPartner.objects.all()
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        partner = models.Partner.objects.filter(user=request.user)
        if not request.user.is_superuser:
            if db_field.name == 'partner':
                    kwargs['queryset'] = partner
            if db_field.name == 'connected_partner':
                    partner_id = models.ConnectedPartner.objects.filter(connected_partner=partner).values('partner')
                    connected_partner_id = models.ConnectedPartner.objects.filter(partner=partner).values('connected_partner')
                    kwargs['queryset'] = models.Partner.objects.filter(id__in=partner_id) | models.Partner.objects.filter(id__in=connected_partner_id) & models.Partner.objects.exclude(id=partner)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class BaseProductAdmin(admin.ModelAdmin):
    list_display=('manufacturer','code','name','packing','category')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('partner','product_partner','base','selling_price','is_active')

    def get_queryset(self, request):
        if not request.user.is_superuser:
            partner = models.Partner.objects.filter(user=request.user)
        return models.Product.objects.filter(partner=partner) | models.Product.objects.filter(product_partner=partner)
        return models.Product.all()
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        partner = models.Partner.objects.filter(user=request.user)
        if not request.user.is_superuser:
            if db_field.name == 'partner':
                    kwargs['queryset'] = partner
            if db_field.name == 'product_partner':
                partner_id = models.ConnectedPartner.objects.filter(connected_partner=partner).values('partner')
                connected_partner_id = models.ConnectedPartner.objects.filter(partner=partner).values('connected_partner')
                kwargs['queryset'] = models.Partner.objects.filter(id__in=partner_id) | models.Partner.objects.filter(id__in=connected_partner_id) & models.Partner.objects.exclude(id=partner)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class OrderAdmin(admin.ModelAdmin):
    models = Order
    pass
    list_display = ('order_partner','order_date','invoice_id','order_status','delivery_date','requested_delivery_time','bill_total')
    readonly_fields = (
        'invoice_id',
    )
    class Meta:
        ordering = ['-order_date']

    # def get_form(self, request, obj=None, **kwargs):
    #     exclude = ()
    #     dist = models.Distributor.objects.filter(user=request.user)
    #     man = models.Manufacturer.objects.filter(user=request.user)
    #     ret = models.Retailer.objects.filter(user=request.user)
    #     if dist:
    #         exclude += ('retailer',)
    #     self.exclude = exclude
    #     return super(OrderAdmin, self).get_form(request, obj, **kwargs)
    #
    def get_queryset(self, request):
        if not request.user.is_superuser:
            partner = models.Partner.objects.filter(user=request.user)
        return models.Order.objects.filter(partner=partner)
        return models.Order.objects.all()

    # def make_id(self):
    #     q = Order.objects.values_list('id', flat=True).order_by('-id')[:1]
    #     if len(q):
    #         self.number = str(self.id) if self.id else str(int(q.get()) + 1)
    #     else:
    #         self.number = 1
    #     return "SEDIST" + str(self.distributor_id) + "RET" + str(self.retailer_id) + "-" + str(self.number)
    #
    # def __str__(self):
    #     return "{}".format(self.id, self.retailer)
    #
    # def save(self, *args, **kwargs):
    #     if not self.invoice_id:
    #         self.invoice_id = self.make_id()
    #     if not self.retailer:
    #         self.retailer = models.Retailer.objects.filter(user=request.user)
    #     super(Order, self).save(*args, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        partner = models.Partner.objects.filter(user=request.user)
        if not request.user.is_superuser:
            if db_field.name == 'partner':
                kwargs['queryset'] = partner
            if db_field.name == 'order_partner':
                partner_id = models.ConnectedPartner.objects.filter(connected_partner=partner).values('partner')
                connected_partner_id = models.ConnectedPartner.objects.filter(partner=partner).values(
                'connected_partner')
                kwargs['queryset'] = models.Partner.objects.filter(id__in=partner_id) | models.Partner.objects.filter(
                id__in=connected_partner_id) & models.Partner.objects.exclude(id=partner)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OrderItemAdmin(admin.ModelAdmin):
    pass
    list_display = ('order_id', 'product', 'item_quantity')

    def get_queryset(self, request):
        if not request.user.is_superuser:
            partner = models.Partner.objects.filter(user=request.user)
            order = models.Order.objects.filter(partner=partner)
            return models.OrderItem.objects.filter(order__in=order)
        return models.OrderItem.objects.all()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        partner = models.Partner.objects.filter(user=request.user)
        if not request.user.is_superuser:
                if db_field.name == 'order':
                    kwargs['queryset'] = models.Order.objects.filter(partner=partner)
                if db_field.name == 'product':
                    kwargs["queryset"] = models.Product.objects.filter(partner__in=partner) | models.Product.objects.filter(product_partner__in=partner)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(models.Partner,PartnerAdmin)
admin.site.register(models.ConnectedPartner,ConnectedPartnerAdmin)
admin.site.register(models.BaseProduct,BaseProductAdmin)
admin.site.register(models.Product,ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
