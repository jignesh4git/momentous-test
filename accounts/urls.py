from django.conf.urls import url, include
from .views import custom_login, register, profile, logout_view


urlpatterns =[
    url(r'^login/$', custom_login, name="login"),
    url(r'^logout/$', logout_view, name="logout"),
    url(r'^register/$',register, name="register"),
    url(r'^profile/$', profile, name="profile"),
  ]  

