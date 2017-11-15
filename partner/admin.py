from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Distributor)
admin.site.register(models.Retailer)
admin.site.register(models.ConnectedRetailer)

admin.site.register(models.Product)

admin.site.register(models.Order)
admin.site.register(models.OrderItem)
# admin.site.register(models.UserProfile)
