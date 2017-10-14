from django.conf.urls import url, include
from partner import models
from . import data_serializers
from rest_framework import routers, serializers, viewsets


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
        distributer_id = self.request.query_params['id']
        return models.Product.objects.filter(distributer__user_id__exact=distributer_id)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'distributer', DistributerViewSet)
router.register(r'product', ProductViewSet, base_name='Product')

# Wire up our API using automatic URL routing.
urlpatterns = [
    url(r'^', include(router.urls)),
]
