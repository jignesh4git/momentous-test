# Create your views here.

from partner import models
from . import data_serializers

from rest_framework import viewsets


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = data_serializers.UserSerializer


# ViewSets define the view behavior.
class DistributerViewSet(viewsets.ModelViewSet):
    queryset = models.Distributer.objects.all()
    serializer_class = data_serializers.DistributerSerializer


# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = data_serializers.ProductSerializer

    def get_queryset(self):
        distributor_id = self.request.query_params['id']
        return models.Product.objects.filter(distributer__user_id__exact=distributor_id)
