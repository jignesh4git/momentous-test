from rest_framework import serializers
from partner import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'email', 'is_staff')


class DistributerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Distributer
        user = UserSerializer()
        fields = ('user', 'company_name', 'company_address')


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Product
        fields = ('id', 'code', 'name', 'packing', 'category')
