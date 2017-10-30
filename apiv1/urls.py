from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views
from .views import DistributerViewSet, ProductViewSet, place_order

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'distributor', DistributerViewSet)
router.register(r'product', ProductViewSet, base_name='Product')

# Wire up our API using automatic URL routing.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', views.obtain_auth_token),
    url(r'place_order/', place_order)
]
