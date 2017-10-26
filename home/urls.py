
from django.conf.urls import url, include
from django.views import generic

from . import views


urlpatterns = [
    url('^$', views.index, name="index"),
]