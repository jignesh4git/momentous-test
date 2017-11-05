from rest_framework import serializers
from partner import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class DistributerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Distributer
        user = UserSerializer()
        fields = ('user', 'company_name', 'mobile_number', 'company_address')


class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Retailer
        user = UserSerializer()
        fields = ('user', 'store_name', 'mobile_number', 'store_address')


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Product
        fields = ('id', 'code', 'name', 'packing', 'category')


class RetailerMinimalDataSerializer(serializers.Serializer):
    store_number = serializers.CharField()
    store_name = serializers.CharField()
    mobile_number = serializers.CharField()
    store_address = serializers.CharField()
    pin_code = serializers.CharField()
    GSTIN = serializers.CharField()
    PAN = serializers.CharField()

    user = UserSerializer()


class DistributorAccountSerializer(serializers.Serializer):
    company_name = serializers.CharField()
    company_address = serializers.CharField()
    mobile_number = serializers.CharField()
    pin_code = serializers.CharField()
    GSTIN = serializers.CharField()
    PAN = serializers.CharField()

    user = UserSerializer()


class RetailerAccountSerializer(serializers.Serializer):
    distributer = DistributerSerializer()
    store_number = serializers.CharField()
    store_name = serializers.CharField()
    mobile_number = serializers.CharField()
    store_address = serializers.CharField()
    pin_code = serializers.CharField()
    GSTIN = serializers.CharField()
    PAN = serializers.CharField()

    user = UserSerializer()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        retailer = RetailerSerializer()
        distributer = DistributerSerializer()
        fields = ('id', 'order_date', 'order_status', 'item_total', 'retailer', 'distributer')
