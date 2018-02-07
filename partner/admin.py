from django import forms
from django.contrib import admin
from . import models
from .models import Order
from django.contrib.auth.models import Group

# Register your models here.
class PartnerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">accessibility</i>'
    list_display=('company_name','type','mobile_number','address','GSTIN')

    def get_queryset(self, request):
         partner = models.Partner.objects.filter(user=request.user)
         emp = models.Employee.objects.filter(user=request.user).values('partner')
         if emp:
             partner = emp
         partner_type = models.Partner.objects.filter(user=request.user).values('type')
         if not request.user.is_superuser and partner_type != "manufacturer":
             return models.Partner.objects.filter(id__in=partner)
         return models.Partner.objects.all()

class EmployeeAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">face</i>'
    list_display=('partner','user','first_name','last_name','mobile_no','permissions')

    def get_queryset(self, request):
        if not request.user.is_superuser:
            partner = models.Partner.objects.filter(user=request.user)
            return models.Employee.objects.filter(partner=partner)
        return  models.Employee.objects.all()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        partner = models.Partner.objects.filter(user=request.user)
        if not request.user.is_superuser:
            if db_field.name == 'partner':
                    partner_id = models.ConnectedPartner.objects.filter(connected_partner=partner).values('partner')
                    connected_partner_id = models.ConnectedPartner.objects.filter(partner=partner).values('connected_partner')
                    kwargs['queryset'] = models.Partner.objects.filter(id__in=partner_id) | models.Partner.objects.filter(id__in=connected_partner_id) | models.Partner.objects.filter(id=partner)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class ConnectedPartnerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">group</i>'
    list_display=('partner','connected_partner','credit_limit','remaining')

    def get_queryset(self, request):
        partner = models.Partner.objects.filter(user=request.user)
        emp = models.Employee.objects.filter(user=request.user).values('partner')
        if emp:
            partner = emp
        if not request.user.is_superuser:
           # partner = models.Partner.objects.filter(user=request.user)
             return models.ConnectedPartner.objects.filter(partner=partner) | models.ConnectedPartner.objects.filter(connected_partner__in=partner)
        return models.ConnectedPartner.objects.all()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        partner = models.Partner.objects.filter(user=request.user)
        emp = models.Employee.objects.filter(user=request.user).values('partner')
        if emp:
            partner = emp
        if not request.user.is_superuser:
            if db_field.name == 'partner':
                    kwargs['queryset'] = models.Partner.objects.filter(id__in=partner)
            if db_field.name == 'connected_partner':
                    partner_id = models.ConnectedPartner.objects.filter(connected_partner=partner).values('partner')
                    connected_partner_id = models.ConnectedPartner.objects.filter(partner=partner).values('connected_partner')
                    kwargs['queryset'] = models.Partner.objects.exclude(id__in=partner_id) & models.Partner.objects.exclude(id__in=connected_partner_id) & models.Partner.objects.exclude(id=partner)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class BaseProductAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">add_circle</i>'
    list_display=('manufacturer','code','name','packing','category')
    def get_queryset(self, request):
        emp = models.Employee.objects.filter(user=request.user).values('partner')
        if not request.user.is_superuser:
            partner = models.Partner.objects.filter(user=request.user)
            connected_partner = models.ConnectedPartner.objects.filter(partner=partner).values('connected_partner')
            if emp:
                partner = emp
            return models.BaseProduct.objects.filter(manufacturer=partner) | models.BaseProduct.objects.filter(manufacturer__in=connected_partner)
        return models.BaseProduct.objects.all()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        partner = models.Partner.objects.filter(user=request.user)
        emp = models.Employee.objects.filter(user=request.user).values('partner')
        if emp:
            partner = emp
        if not request.user.is_superuser:
            if db_field.name == 'manufacturer':
                kwargs['queryset'] = models.Partner.objects.filter(id__in=partner)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class ProductAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">add</i>'
    list_display = ('partner','connected_partner','base','selling_price','is_active')
    list_filter = ('connected_partner',)
    def get_queryset(self, request):
        emp = models.Employee.objects.filter(user=request.user).values('partner')
        if not request.user.is_superuser:
            partner = models.Partner.objects.filter(user=request.user)
            connected_partner = models.ConnectedPartner.objects.filter(partner=partner).values('connected_partner')
            if emp:
                partner = emp
            return models.Product.objects.filter(partner=partner) | models.Product.objects.filter(connected_partner__in=connected_partner)
        return models.Product.objects.all()
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        partner = models.Partner.objects.filter(user=request.user)
        manufacturer = models.Partner.objects.filter(user=request.user,type="manufacturer")
        emp = models.Employee.objects.filter(user=request.user).values('partner')
        if emp:
            partner = emp
            manufacturer = models.Partner.objects.filter(id__in=partner,type="manufacturer")
        if not request.user.is_superuser:
            if db_field.name == 'partner':
                    kwargs['queryset'] = models.Partner.objects.filter(id__in=partner)
            if db_field.name == 'connected_partner':
                partner_id = models.ConnectedPartner.objects.filter(connected_partner=partner).values('partner')
                connected_partner_id = models.ConnectedPartner.objects.filter(partner=partner).values('connected_partner')
                kwargs['queryset'] = models.Partner.objects.filter(id__in=partner_id) | models.Partner.objects.filter(id__in=connected_partner_id) & models.Partner.objects.exclude(id=partner)
            if db_field.name == 'base':

                baseproduct_id = models.Product.objects.filter(partner__in=partner).values('base') | models.Product.objects.filter(connected_partner__in=partner).values('base')
                if manufacturer:
                    kwargs['queryset'] = models.BaseProduct.objects.filter(manufacturer=partner)
                else :
                    kwargs['queryset'] = models.BaseProduct.objects.filter(id__in=baseproduct_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class OrderAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">add_circle</i>'
    models = Order
    pass
    list_display = ('order_date','invoice_id','order_status','delivery_date','requested_delivery_time','bill_total')
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
        emp = models.Employee.objects.filter(user=request.user).values('partner')
        if not request.user.is_superuser:
            partner = models.Partner.objects.filter(user=request.user)
            if emp:
                partner = emp
            return models.Order.objects.filter(partner=partner)  | models.Order.objects.filter(connected_partner=partner)
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
        emp = models.Employee.objects.filter(user=request.user).values('partner')
        partner = models.Partner.objects.filter(user=request.user)
        if emp:
            partner = emp
        if not request.user.is_superuser:
            if db_field.name == 'partner':
                kwargs['queryset'] = models.Partner.objects.filter(id__in=partner)
            if db_field.name == 'connected_partner':
                partner_id = models.ConnectedPartner.objects.filter(connected_partner=partner).values('partner')
                connected_partner_id = models.ConnectedPartner.objects.filter(partner=partner).values(
                'connected_partner')
                kwargs['queryset'] = models.Partner.objects.filter(id__in=partner_id) | models.Partner.objects.filter(
                id__in=connected_partner_id) & models.Partner.objects.exclude(id=partner)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OrderItemAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">add</i>'
    pass
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        partner = models.Partner.objects.filter(user=request.user)
        emp = models.Employee.objects.filter(user=request.user).values('partner')
        if emp:
            partner = emp
        if not request.user.is_superuser:
                if db_field.name == 'order':
                    kwargs['queryset'] = models.Order.objects.filter(partner=partner)
                if db_field.name == 'product':
                    kwargs["queryset"] = models.Product.objects.filter(partner__in=partner) | models.Product.objects.filter(connected_partner__in=partner)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(models.Partner,PartnerAdmin)
admin.site.register(models.ConnectedPartner,ConnectedPartnerAdmin)
admin.site.register(models.BaseProduct,BaseProductAdmin)
admin.site.register(models.Product,ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
admin.site.register(models.Employee,EmployeeAdmin)
