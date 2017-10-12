from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


# Create your models here.

class partner(models.Model):
    name = models.CharField(max_length=250)


class Distributer(models.Model):
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
    distributer = models.ForeignKey(Distributer)

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
    retailer = models.ForeignKey(Retailer)
    distributer = models.ForeignKey(Distributer)
    order_date = models.DateField(auto_created=True)
    order_status = models.CharField(max_length=255, blank=False)
    # requested_delivery_time = models.DateField(blank=True)
    item_total = models.CharField(max_length=255, blank=True)
    s_gst = models.CharField(max_length=255, blank=True)
    c_gst = models.CharField(max_length=255, blank=True)
    other_charge_description = models.CharField(max_length=255, blank=True)
    other_charge = models.CharField(max_length=255, blank=True)
    bill_total = models.CharField(max_length=255, blank=True)

    # delivery_date = models.DateField(blank=True)

    def __str__(self):
        return "{}".format(self.id, self.order_date)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product)
    item_quantity = models.IntegerField()

    # item_price = models.IntegerField(blank=True)
    # total = models.IntegerField(blank=True)
    # offer_id = models.CharField(max_length=25, blank=True)
    # s_gst = models.CharField(max_length=255, blank=True)
    # c_gst = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "{}".format(self.order_id, self.id, self.product_id)


class ConnectedRetailer(models.Model):
    distributer = models.ForeignKey(Distributer, on_delete=models.CASCADE)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    credit_limit = models.IntegerField()
    remaining = models.IntegerField()

    def __str__(self):
        return "{}".format(self.distributer, self.retailer)  

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    #contactno = models.IntegerField(blank=True)
    # more model fields as needed

    def __str__(self):
        return "{}".format(self.user)

     

