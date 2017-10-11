
from django.conf.urls import url, include
from django.views import generic

from . import views


urlpatterns = [
    url('^$', generic.TemplateView.as_view(template_name="home/index.html"), name="index"),
]