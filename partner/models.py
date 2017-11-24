from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.contrib import admin


# Create your models here.

class Partner(models.Model):
    name = models.CharField(max_length=250)
class Distributor(models.Model):
    user = models.OneToOneField(User)
    mobile_number = PhoneNumberField()

    company_name = models.CharField(max_length=255, blank=False)
    company_address = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=255)

    GSTIN = models.CharField(max_length=255, blank=True)
    PAN = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "{}".format(self.company_name)

class Retailer(models.Model):
    user = models.OneToOneField(User)
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255, blank=False)
    store_number = PhoneNumberField()
    mobile_number = PhoneNumberField(blank=True)

    store_address = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=255)
    GSTIN = models.CharField(max_length=255, blank=True)
    PAN = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return "{}".format(self.store_name, self.store_number)

class Product(models.Model):
    distributor = models.ForeignKey(Distributor)
    code = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=False)
    packing = models.CharField(max_length=255, blank=False)
    price = models.CharField(max_length=255, blank=True)
    offer_id = models.CharField(max_length=255, blank=True)
    active = models.BooleanField()
    category = models.CharField(max_length=255, blank=True)
    HSN = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "{}".format(self.name, self.packing)

class Order(models.Model):
    retailer = models.ForeignKey(Retailer, related_name='retailer')
    distributor = models.ForeignKey(Distributor, related_name='distributor')
    order_date = models.DateField(auto_created=True)
    order_status = models.CharField(max_length=255, blank=False)
    # requested_delivery_time = models.DateField(blank=True)
    item_total = models.CharField(max_length=255, blank=True)
    s_gst = models.CharField(max_length=255, blank=True)
    c_gst = models.CharField(max_length=255, blank=True)
    other_charge_description = models.CharField(max_length=255, blank=True)
    other_charge = models.CharField(max_length=255, blank=True)
    bill_total = models.CharField(max_length=255, blank=True)
    invoice_id = models.CharField(max_length=255)
    # delivery_date = models.DateField(blank=True)
    # Metadata
    # class Meta:
        # ordering = ["-order_date"]
    def make_id(self):
        q = Order.objects.values_list('id', flat=True).order_by('-id')[:1]
        if len(q):
            self.number = str(self.id) if self.id else str(int(q.get()) + 1)
        else:
            self.number = 1
        return "SEDIST"+str(self.distributor_id)+"RET"+str(self.retailer_id)+"-"+str(self.number)
    def __str__(self):
            return "{}".format(self.id, self.retailer)
    def save(self,*args,**kwargs):
        if not self.invoice_id:
            self.invoice_id = self.make_id()
        super(Order,self).save(*args,**kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)    
    product = models.ForeignKey(Product)
    item_quantity = models.IntegerField()
    # item_price = models.IntegerField(blank=True)
    # total = models.IntegerField(blank=True)
    # offer_id = models.CharField(max_length=25, blank=True)
    # s_gst = models.CharField(max_length=255, blank=True)
    # c_gst = models.CharField(max_length=255, blank=True)
    class Meta:
        verbose_name_plural ="Invoices"  
    def __str__(self):
        return "{}".format(self.order_id, self.id, self.product_id)

class ConnectedRetailer(models.Model):
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    credit_limit = models.IntegerField()
    remaining = models.IntegerField()

    def __str__(self):
        return "{}".format(self.distributor, self.retailer)

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    # contactno = models.IntegerField(blank=False)
    # more model fields as needed

    def __unicode__(self):
        return self.user.username