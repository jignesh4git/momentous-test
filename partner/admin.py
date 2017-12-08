from django import forms
from django.contrib import admin
from . import models
from .models import Order
from django.contrib.auth.models import Group

# Register your models here.

class ManufacturerAdmin(admin.ModelAdmin):
    pass
    list_display = ('company_name', 'company_address')

    def get_queryset(self, request):
        if not request.user.is_superuser:
            return models.Manufacturer.objects.filter(user=request.user)
        return models.Manufacturer.objects.all()
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'user':
                dist_user_id = models.Distributor.objects.distinct('user').values('user')
                manif_user_id = models.Manufacturer.objects.distinct('user').values('user')
                kwargs['queryset'] = models.User.objects.exclude(id__in=dist_user_id) & models.User.objects.exclude(
                    id__in=manif_user_id) & models.User.objects.exclude(id=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DistributorAdmin(admin.ModelAdmin):
    pass
    list_display = ('company_name', 'company_address')

    def get_queryset(self, request):
        if not request.user.is_superuser:
            manufacturer = models.Manufacturer.objects.filter(user=request.user)
            return models.Distributor.objects.filter(user=request.user) | models.Distributor.objects.filter(manufacturer__in = manufacturer)
        return models.Distributor.objects.all()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'user':
                ret_user_id = models.Retailer.objects.distinct('user').values('user')
                dist_user_id = models.Distributor.objects.distinct('user').values('user')
                kwargs['queryset'] = models.User.objects.exclude(id__in=ret_user_id) & models.User.objects.exclude(
                    id__in=dist_user_id) & models.User.objects.exclude(id=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class RetailerAdmin(admin.ModelAdmin):
    pass
    list_display = ('store_name', 'store_number', 'store_address', 'user')

    def get_queryset(self, request):
        if not request.user.is_superuser:
            distributor = models.Distributor.objects.filter(user=request.user)
            return models.Retailer.objects.filter(distributor=distributor)
        return models.Retailer.objects.all()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'user':
                dist = models.Distributor.objects.filter(user=request.user)
                if dist:
                    dist_user_id = models.Distributor.objects.distinct('user').values('user')
                    ret_user_id = models.Retailer.objects.distinct('user').values('user')
                kwargs['queryset'] = models.User.objects.filter(id__in=ret_user_id) & models.User.objects.filter(
                    id__in=dist_user_id) & models.User.objects.exclude(id=1)
            if db_field.name == 'distributor':
                kwargs['queryset'] = models.Distributor.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ConnectedRetailerAdmin(admin.ModelAdmin):
    list_display = ('retailer', 'remaining')

    def get_queryset(self, request):
        if not request.user.is_superuser:
            distributor = models.Distributor.objects.filter(user=request.user)
            return models.ConnectedRetailer.objects.filter(distributor=distributor)
        return models.ConnectedRetailer.objects.all()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        dist = models.Distributor.objects.filter(user=request.user)
        if not request.user.is_superuser:
            if db_field.name == "distributor":
                kwargs["queryset"] = dist
            if db_field.name == "retailer":
                kwargs["queryset"] = models.Retailer.objects.filter(distributor=dist)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ConnectedDistributorAdmin(admin.ModelAdmin):
    list_display = ('distributor', 'remaining')

    def get_queryset(self, request):
        if not request.user.is_superuser:
            manufacturer = models.Manufacturer.objects.filter(user=request.user)
            return models.ConnectedDistributor.objects.filter(manufacturer=manufacturer)
        return models.ConnectedDistributor.objects.all()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        manuf = models.Manufacturer.objects.filter(user=request.user)
        if not request.user.is_superuser:
            if db_field.name == "manufacturer":
                kwargs["queryset"] = manuf
            if db_field.name == "distributor":
                kwargs["queryset"] = models.Distributor.objects.filter(manufacturer=manuf)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'packing', 's_gst', 'c_gst','active')

    # def get_queryset(self, request):
    #     manufacturer = models.Manufacturer.objects.filter(user=request.user)
    #     distributor = models.Distributor.objects.filter(user=request.user)
    #     retailer = models.Retailer.objects.filter(user=request.user)
    #     if not request.user.is_superuser:
    #         if retailer:
    #             distributor = models.ConnectedRetailer.objects.filter(retailer=retailer).values('distributor')
    #         return models.Product.objects.filter(manufacturer__in=manufacturer) | models.Product.objects.filter(distributor__in=distributor)
    #     return models.Product.objects.all()
    #
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     dist = models.Distributor.objects.filter(user=request.user)
    #     ret = models.Retailer.objects.filter(user=request.user)
    #     if not request.user.is_superuser:
    #         if dist:
    #             if db_field.name == 'distributor':
    #                 kwargs['queryset'] = models.Distributor.objects.filter(user=request.user)
    #         if ret:
    #             if db_field.name == 'distributor':
    #                 dist = models.ConnectedRetailer.objects.filter(retailer=ret).values('distributor')
    #                 kwargs['queryset'] = models.Distributor.objects.filter(id__in=dist)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

class DistributorProductAdmin(admin.ModelAdmin):
    list_display = ('distributor','product','price','offer_id','final_price', 'active')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        man = models.Manufacturer.objects.filter(user=request.user)
        if not request.user.is_superuser:
            if man:
                if db_field.name == 'distributor':
                    dist = models.ConnectedDistributor.objects.filter(manufacturer=man).values('distributor')
                    kwargs['queryset'] = models.Distributor.objects.filter(id__in=dist)
                if db_field.name == 'product':
                    kwargs['queryset'] = models.Product.objects.filter(active='t')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class RetailerProductAdmin(admin.ModelAdmin):
    list_display = ('retailer','product','price','offer_id','final_price', 'active')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        dist = models.Distributor.objects.filter(user=request.user)
        man = models.Manufacturer.objects.filter(user=request.user)
        if not request.user.is_superuser:
            if dist:
                if db_field.name == 'distributor':
                    kwargs['queryset'] = dist;
                if db_field.name == 'retailer':
                    ret = models.ConnectedRetailer.objects.filter(distributor=dist).values('retailer')
                    kwargs['queryset'] = models.Retailer.objects.filter(id__in=ret)
                if db_field.name == 'product':
                    product_id = models.DistributorProduct.objects.filter(active='t')
                    kwargs['queryset'] = models.Product.objects.filter(id__in=product_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class OrderAdmin(admin.ModelAdmin):
    pass
    list_display = ('order_date', 'invoice_id', 'retailer', 'order_status', 'bill_total')
    readonly_fields = (
        'invoice_id',
    )
    class Meta:
        ordering = ["-order_date"]

    def get_form(self, request, obj=None, **kwargs):
        exclude = ()
        dist = models.Distributor.objects.filter(user=request.user)
        man = models.Manufacturer.objects.filter(user=request.user)
        ret = models.Retailer.objects.filter(user=request.user)
        if dist:
            exclude += ('retailer',)
        self.exclude = exclude
        return super(OrderAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        if not request.user.is_superuser:
            manufacturer = models.Manufacturer.objects.filter(user=request.user)
            distributor = models.Distributor.objects.filter(user=request.user)
            retailer = models.Retailer.objects.filter(user=request.user)
            return models.Order.objects.filter(manufacturer = manufacturer) | models.Order.objects.filter(distributor=distributor) | models.Order.objects.filter(retailer=retailer)
        return models.Order.objects.all()

    def make_id(self):
        q = Order.objects.values_list('id', flat=True).order_by('-id')[:1]
        if len(q):
            self.number = str(self.id) if self.id else str(int(q.get()) + 1)
        else:
            self.number = 1
        return "SEDIST" + str(self.distributor_id) + "RET" + str(self.retailer_id) + "-" + str(self.number)

    def __str__(self):
        return "{}".format(self.id, self.retailer)

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            self.invoice_id = self.make_id()
        if not self.retailer:
            self.retailer = models.Retailer.objects.filter(user=request.user)
        super(Order, self).save(*args, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        dist = models.Distributor.objects.filter(user=request.user)
        ret = models.Retailer.objects.filter(user=request.user)
        if not request.user.is_superuser:
            if dist:
                if db_field.name == "distributor":
                    kwargs["queryset"] = dist
                if db_field.name == "retailer":
                    retailer_id = models.ConnectedRetailer.objects.filter(distributor=dist).values('retailer')
                    kwargs["queryset"] = models.Retailer.objects.filter(id__in=retailer_id)
                if db_field.name == 'product':
                    kwargs['queryset'] = models.DistributorProduct.objects.filter(active='t')
            if ret:
                if db_field.name == "retailer":
                    kwargs["queryset"] = ret
                if db_field.name == "distributor":
                    distributor_id = models.ConnectedRetailer.objects.filter(retailer=ret).values('distributor')
                    kwargs["queryset"] = models.Distributor.objects.filter(id__in=distributor_id)
                if db_field.name == 'product':
                    kwargs['queryset'] = models.RetailerProduct.objects.filter(active='t')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OrderItemAdmin(admin.ModelAdmin):
    pass
    list_display = ('order_id', 'product', 'item_quantity')

    def get_queryset(self, request):
        if not request.user.is_superuser:
            distributor = models.Distributor.objects.filter(user=request.user)
            retailer = models.Retailer.objects.filter(user=request.user)
            order = models.Order.objects.filter(distributor=distributor) | models.Order.objects.filter(
                retailer=retailer)
            return models.OrderItem.objects.filter(order__in=order)
        return models.OrderItem.objects.all()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        dist = models.Distributor.objects.filter(user=request.user)
        ret = models.Retailer.objects.filter(user=request.user)
        if not request.user.is_superuser:
            if ret:
                if db_field.name == 'order':
                    kwargs['queryset'] = models.Order.objects.filter(retailer=ret)
                if db_field.name == 'product':
                        distributor_id = models.ConnectedRetailer.objects.filter(retailer=ret).values('distributor')
                        product_id = models.RetailerProduct.objects.filter(distributor=distributor_id).values('product')
                        kwargs["queryset"] = models.Product.objects.filter(id__in=product_id)
            if dist:
                if db_field.name == 'order':
                    kwargs['queryset'] = models.Order.objects.filter(distributor=dist)
                if db_field.name == 'product':
                        product_id = models.DistributorProduct.objects.filter(distributor=dist).values('product')
                        kwargs["queryset"] = models.Product.objects.filter(id__in=product_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(models.Manufacturer, ManufacturerAdmin)
admin.site.register(models.Distributor, DistributorAdmin)
admin.site.register(models.Retailer, RetailerAdmin)
admin.site.register(models.ConnectedRetailer, ConnectedRetailerAdmin)
admin.site.register(models.ConnectedDistributor, ConnectedDistributorAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.DistributorProduct, DistributorProductAdmin)
admin.site.register(models.RetailerProduct, RetailerProductAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)