from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


class Partner(models.Model):
    PARTNER_TYPE = (
        ('manufacturer', 'Manufacturer'),
        ('distributor', 'Distributor'),
        ('retailer', 'Retailer'),
        ('employee', 'Employee'),
    )

    PERMISSIONS = (
        ('sell_product', 'Sell Product'),
        ('sell_add_product', 'Add & Sell Product'),
        ('sell_add_product_partner', 'Add & Sell Product, Add Partner'),
    )

    user = models.OneToOneField(User)
    mobile_number = PhoneNumberField()
    alternate_number = PhoneNumberField()
    company_name = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=255)
    GSTIN = models.CharField(max_length=255, blank=True)
    PAN = models.CharField(max_length=255, blank=True)
    ADHAAR = models.CharField(max_length=255, blank=True)

    type = models.CharField(max_length=255, choices=PARTNER_TYPE, blank=False)
    buys_from = models.ManyToManyField('self')
    sells_to = models.ManyToManyField('self')

    permissions = models.CharField(max_length=255, choices=PERMISSIONS, blank=True)

    def __str__(self):
        return "{}".format(self.company_name)


class BaseProduct(models.Model):
    manufacturer = models.ForeignKey(Partner, null=True)
    code = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=False)
    packing = models.CharField(max_length=255, blank=False)
    GST_CHOICES = (
        (0, '0'),
        (5, '5'),
        (12, '12'),
        (18, '18'),
        (28, '28'),
    )
    s_gst = models.IntegerField(choices=GST_CHOICES, default=0)
    c_gst = models.IntegerField(choices=GST_CHOICES, default=0)
    category = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "{}".format(self.name, self.manufacturer, self.packing)


class Product(models.Model):
    base = models.ForeignKey(BaseProduct)
    selling_price = models.FloatField()
    is_active = models.BooleanField()


class Order(models.Model):
    order_from = models.ForeignKey(Partner)
    order_to = models.ForeignKey(Partner)

    order_status = models.CharField(max_length=255, blank=False)
    order_date = models.DateField(auto_created=True)
    delivery_date = models.DateField(blank=True)

    requested_delivery_time = models.DateField(blank=True)
    item_total = models.CharField(max_length=255, blank=True)
    s_gst_total = models.CharField(max_length=255, blank=True)
    c_gst_total = models.CharField(max_length=255, blank=True)
    other_charge_description = models.CharField(max_length=255, blank=True)
    other_charge = models.CharField(max_length=255, blank=True)
    bill_total = models.CharField(max_length=255, blank=True)
    invoice_id = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-order_date"]

    def make_id(self):
        q = Order.objects.values_list('id', flat=True).order_by('-id')[:1]
        if len(q):
            self.number = str(self.id) if self.id else str(int(q.get()) + 1)
        else:
            self.number = 1
        return "SEFRM" + str(self.order_from.user.id) + "TO" + str(self.order_to.user.id) + "-" + str(self.number)

    def __str__(self):
        return "{}".format(self.id)

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            self.invoice_id = self.make_id()
        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product)
    item_quantity = models.IntegerField()

    total = models.IntegerField(blank=True)
    # offer_id = models.CharField(max_length=25, blank=True)
    # change to offer
    s_gst = models.CharField(max_length=255, blank=True)
    c_gst = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "Invoices"

    def __str__(self):
        return "{}".format(self.order_id, self.id, self.product_id)


class ConnectedPartner(models.Model):
    first_partner = models.ForeignKey(Partner)
    second_partner = models.ForeignKey(Partner)
    credit_limit = models.IntegerField()
    remaining = models.IntegerField()

    def __str__(self):
        return "{}".format(self.first_partner, self.second_partner)


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    # contactno = models.IntegerField(blank=False)
    # more model fields as needed

    def __unicode__(self):
        return self.user.username
