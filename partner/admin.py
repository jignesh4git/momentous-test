from django.contrib import admin
from . import models

# Register your models here.

class DistributorAdmin(admin.ModelAdmin):
    pass
    list_display = ('company_name','company_address')
    def get_queryset(self, request):
        if not request.user.is_superuser:
            return models.Distributor.objects.filter(user=request.user)
        return models.Distributor.objects.all()
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'user':
                ret_user_id = models.Retailer.objects.distinct('user').values('user')
                dist_user_id = models.Distributor.objects.distinct('user').values('user')
                kwargs['queryset'] = models.User.objects.exclude(id__in= ret_user_id) & models.User.objects.exclude(id__in = dist_user_id) & models.User.objects.exclude(id = 1)
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
                ret_user_id = models.Retailer.objects.distinct('user').values('user')
                dist_user_id = models.Distributor.objects.distinct('user').values('user')
                kwargs['queryset'] = models.User.objects.exclude(id__in= ret_user_id) & models.User.objects.exclude(id__in = dist_user_id) & models.User.objects.exclude(id = 1)
            if db_field.name == 'distributor':
                kwargs['queryset'] = models.Distributor.objects.filter(user = request.user)
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

class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'packing', 'price', 's_gst', 'c_gst', 'final_price','offer_id', 'active')
    def get_queryset(self, request):
        distributor = models.Distributor.objects.filter(user=request.user)
        retailer = models.Retailer.objects.filter(user=request.user)
        if not request.user.is_superuser:
            if retailer:
                distributor = models.ConnectedRetailer.objects.filter(retailer=retailer).values('distributor')
            return models.Product.objects.filter(distributor__in=distributor)
        return models.Product.objects.all()
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        dist = models.Distributor.objects.filter(user=request.user)
        ret = models.Retailer.objects.filter(user=request.user)
        if not request.user.is_superuser:
            if dist:
                if db_field.name == 'distributor':
                    kwargs['queryset'] = models.Distributor.objects.filter(user = request.user)
            if ret:
                if db_field.name == 'distributor':
                    dist = models.ConnectedRetailer.objects.filter(retailer=ret).values('distributor')
                    kwargs['queryset'] = models.Distributor.objects.filter(id__in=dist)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class OrderAdmin(admin.ModelAdmin):
    # distributor = models.ForeignKey(Distributor, related_name="dconnects",related_query_name="dconnect")
    # retailer = models.ForeignKey(Retailer, related_name="rconnects",related_query_name="rconnect")
    pass
    list_display = ('order_date', 'invoice_id', 'retailer', 'order_status', 'bill_total')
    readonly_fields = (
        'invoice_id',
    )
    class Meta:
        ordering = ["-order_date"]
    def get_queryset(self, request):
        if not request.user.is_superuser:
            distributor = models.Distributor.objects.filter(user=request.user)
            retailer = models.Retailer.objects.filter(user=request.user)
            return models.Order.objects.filter(distributor=distributor) | models.Order.objects.filter(retailer=retailer)
        return models.Order.objects.all()
    def make_id(self):
        q = Order.objects.values_list('id', flat=True).order_by('-id')[:1]
        if len(q):
            self.number = str(self.id) if self.id else str(int(q.get()) + 1)
        else:
            self.number = 1
        return "SEDIST"+str(self.distributor_id)+"RET"+str(self.retailer_id)+"-"+str(self.number)
    def __str__(self):
            return "{}".format(self.id, self.retailer)
    def save(self, *args, **kwargs):
        if not self.invoice_id:
            self.invoice_id = self.make_id()
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
            if ret:
                if db_field.name == "retailer":
                    kwargs["queryset"] = ret
                if db_field.name == "distributor":
                    distributor_id = models.ConnectedRetailer.objects.filter(retailer=ret).values('distributor')
                    kwargs["queryset"] = models.Distributor.objects.filter(id__in=distributor_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class OrderItemAdmin(admin.ModelAdmin):
    pass
    list_display = ('order', 'product', 'item_quantity')
    def get_queryset(self, request):
        if not request.user.is_superuser:
            distributor = models.Distributor.objects.filter(user=request.user)
            retailer = models.Retailer.objects.filter(user=request.user)
            order = models.Order.objects.filter(distributor=distributor) | models.Order.objects.filter(retailer=retailer)
            return models.OrderItem.objects.filter(order__in=order)
        return models.OrderItem.objects.all()
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        dist = models.Distributor.objects.filter(user=request.user)
        ret = models.Retailer.objects.filter(user=request.user)
        if not request.user.is_superuser:
            if db_field.name == 'order':
                kwargs['queryset'] = models.Order.objects.filter(distributor=dist) | models.Order.objects.filter(retailer=ret)
            if db_field.name == 'product':
                if ret:
                    distributor_id = models.ConnectedRetailer.objects.filter(retailer=ret).values('distributor')
                    kwargs["queryset"] = models.Product.objects.filter(distributor=distributor_id)
                else:
                    kwargs['queryset'] = models.Product.objects.filter(distributor=dist)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(models.Distributor,DistributorAdmin)
admin.site.register(models.Retailer,RetailerAdmin)
admin.site.register(models.ConnectedRetailer,ConnectedRetailerAdmin)
admin.site.register(models.Product,ProductAdmin)
admin.site.register(models.Order,OrderAdmin)
admin.site.register(models.OrderItem,OrderItemAdmin)
