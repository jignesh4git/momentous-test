from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views
from .views import DistributorViewSet, ProductViewSet, place_order, get_account, get_connected_retailers, \
    get_orders, get_order_detail, get_invoices

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'distributor', DistributorViewSet)
router.register(r'product', ProductViewSet, base_name='Product')

# Wire up our API using automatic URL routing.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', views.obtain_auth_token),
    url(r'place_order/', place_order),
    url(r'account/', get_account),
    url(r'my_retailers', get_connected_retailers),
    url(r'orders', get_orders),
    url(r'order_detail', get_order_detail),
    url(r'invoices', get_invoices),
]
