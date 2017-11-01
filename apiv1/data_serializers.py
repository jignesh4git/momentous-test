from rest_framework import serializers
from partner import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff')


class DistributerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Distributer
        user = UserSerializer()
        fields = ('user', 'company_name', 'company_address')


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Product
        fields = ('id', 'code', 'name', 'packing', 'category')


class DistributorAccountSerializer(serializers.Serializer):
    company_name = serializers.CharField()
    company_address = serializers.CharField()
    mobile_number = serializers.CharField()
    pin_code = serializers.CharField()
    GSTIN = serializers.CharField()
    PAN = serializers.CharField()

    user = UserSerializer()

class RetailerAccountSerializer(serializers.Serializer):
    distributer = serializers.CharField()
    store_number = serializers.CharField()
    store_name = serializers.CharField()
    mobile_number = serializers.CharField()
    store_address = serializers.CharField()
    pin_code = serializers.CharField()
    GSTIN = serializers.CharField()
    PAN = serializers.CharField()

    user = UserSerializer()

