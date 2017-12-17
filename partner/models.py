from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User, Permission
from django.contrib.auth.models import Group


class Partner(models.Model):
    PARTNER_TYPE = (
        ('manufacturer', 'Manufacturer'),
        ('distributor', 'Distributor'),
        ('retailer', 'Retailer'),
    )

    PERMISSIONS = (
        ('sell_product', 'Sell Product'),
        ('add_product', 'Add Product'),
        ('add_partner', 'Add Partner'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = PhoneNumberField()
    alternate_number = PhoneNumberField()
    company_name = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=255)
    GSTIN = models.CharField(max_length=255, blank=True)
    PAN = models.CharField(max_length=255, blank=True)
    ADHAAR = models.CharField(max_length=255, blank=True)

    type = models.CharField(max_length=255, choices=PARTNER_TYPE, blank=False)
    # buys_from = models.ManyToManyField('self', blank=True)
    # sells_to = models.ManyToManyField('self', blank=True)

    permissions = models.CharField(max_length=255, choices=PERMISSIONS, blank=True)

    # offered_products = models.ManyToManyField(BaseProduct, blank=True)

    def __str__(self):
        return "{}".format(self.company_name)


class ConnectedPartner(models.Model):
    partner = models.ForeignKey(Partner, related_name='partner')
    connected_partner = models.ForeignKey(Partner, related_name='connected_partner')
    credit_limit = models.IntegerField()
    remaining = models.IntegerField()

    def __str__(self):
        return "{}".format(self.connected_partner, self.partner)


class Manufacturer(models.Model):
    user = models.OneToOneField(User)
    mobile_number = PhoneNumberField()
    company_name = models.CharField(max_length=255, blank=False)
    company_address = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=255)
    GSTIN = models.CharField(max_length=255, blank=True)
    PAN = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "{}".format(self.company_name)


class Distributor(models.Model):
    user = models.OneToOneField(User)
    mobile_number = PhoneNumberField()
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True)
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


class BaseProduct(models.Model):
    manufacturer = models.ForeignKey(Partner, on_delete=models.CASCADE)
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

    class Meta:
        verbose_name_plural = "Product Master"

    def __str__(self):
        return '%s %s (%s)' % (self.code, self.name, self.manufacturer)


class Product(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    connected_partner = models.ForeignKey(Partner, related_name='product_partner')
    base = models.ForeignKey(BaseProduct, on_delete=models.CASCADE)
    selling_price = models.FloatField()
    is_active = models.BooleanField()

    def __unicode__(self):
        return "{}".format(self.base, self.partner, self.connected_partner)

    def __str__(self):
        return '%s (%s)(%s)' % (self.base, self.connected_partner, self.selling_price)


class Order(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    connected_partner = models.ForeignKey(Partner, related_name='order_partner')
    order_status = models.CharField(max_length=255, blank=False)
    order_date = models.DateField(auto_created=True)
    delivery_date = models.DateField(blank=True, null=True)
    requested_delivery_time = models.DateField(blank=True, null=True)
    item_total = models.CharField(max_length=255, blank=True, null=True)
    s_gst_total = models.CharField(max_length=255, blank=True, null=True)
    c_gst_total = models.CharField(max_length=255, blank=True, null=True)
    other_charge_description = models.CharField(max_length=255, blank=True, null=True)
    other_charge = models.CharField(max_length=255, blank=True, null=True)
    bill_total = models.CharField(max_length=255, blank=True, null=True)
    invoice_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["-order_date"]

    def make_id(self):
        q = Order.objects.values_list('id', flat=True).order_by('-id')[:1]
        if len(q):
            self.number = str(self.id) if self.id else str(int(q.get()) + 1)
        else:
            self.number = 1
        return "SEFRM" + str(self.partner.id) + "TO" + str(self.connected_partner.id) + "-" + str(self.number)

    def __str__(self):
        return "{}".format(self.id, self.partner, self.connected_partner)

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            self.invoice_id = self.make_id()
        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    item_quantity = models.IntegerField()

    total = models.IntegerField(blank=True)
    # offer_id = models.CharField(max_length=25, blank=True)
    # change to offer
    s_gst = models.CharField(max_length=255, blank=True)
    c_gst = models.CharField(max_length=255, blank=True)

    # class Meta:
    #     verbose_name_plural = "Invoices"

    def __str__(self):
        return "{}".format(self.order_id, self.id, self.product_id)


class ConnectedRetailer(models.Model):
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    credit_limit = models.IntegerField()
    remaining = models.IntegerField()

    def __str__(self):
        return "{}".format(self.distributor, self.retailer)


class ConnectedDistributor(models.Model):
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    credit_limit = models.IntegerField()
    remaining = models.IntegerField()

    def __str__(self):
        return "{}".format(self.distributor, self.manufacturer)


class Employee(models.Model):
    PERMISSIONS = (
        ('sell_product', 'Sell Product'),
        ('add_product', 'Add Product'),
        ('add_partner', 'Add Partner'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mobile_no = PhoneNumberField(blank=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    permissions = models.CharField(max_length=255, choices=PERMISSIONS, blank=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        u = User.objects.get(username=self.user)
        u.groups.clear()
        u.save()
        u.is_staff = True
        u.save()
        if self.permissions == 'add_product':
            group = Group.objects.get(name='product')
            group.user_set.add(u)
        if self.permissions == 'add_partner':
            group = Group.objects.get(name='partner')
            group.user_set.add(u)
        if self.permissions == 'sell_product':
            group = Group.objects.get(name='order')
            group.user_set.add(u)
        super(Employee, self).save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    # contactno = models.IntegerField(blank=False)
    # more model fields as needed

    def __unicode__(self):
        return self.user.username
