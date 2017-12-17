from rest_framework import serializers
from partner import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Distributor
        user = UserSerializer()
        fields = ('user', 'company_name', 'mobile_number', 'company_address')


class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Retailer
        user = UserSerializer()
        fields = ('user', 'store_name', 'mobile_number', 'store_address')


class PartnerMinimalDataSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()
    company_name = serializers.CharField()
    pin_code = serializers.CharField()


class BaseProductSerializer(serializers.ModelSerializer):
    manufacturer = PartnerMinimalDataSerializer()

    class Meta:
        model = models.BaseProduct
        fields = ('manufacturer', 'code', 'name', 'packing', 's_gst', 'c_gst', 'category')


class ProductSerializer(serializers.ModelSerializer):
    base = BaseProductSerializer()

    class Meta:
        model = models.Product
        fields = ('id', 'selling_price', 'is_active', 'base')


class PartnerAccountSerializer(serializers.Serializer):
    user = UserSerializer()
    mobile_number = serializers.CharField()
    alternate_number = serializers.CharField()
    company_name = serializers.CharField()
    address = serializers.CharField()
    pin_code = serializers.CharField()
    GSTIN = serializers.CharField()
    PAN = serializers.CharField()
    type = serializers.CharField()


class OrderSerializer(serializers.ModelSerializer):
    retailer = PartnerAccountSerializer()
    distributor = PartnerAccountSerializer()

    class Meta:
        model = models.Order
        fields = ('id', 'order_date', 'order_status', 'item_total', 'retailer', 'distributor')


class MinimalProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('id', 'code', 'name', 'packing', 'category')


class OrderItemSerializer(serializers.ModelSerializer):
    product = MinimalProductSerializer()

    class Meta:
        model = models.OrderItem
        fields = ('id', 'item_quantity', 'product')
