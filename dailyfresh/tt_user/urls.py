from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'register/$',views.register),
    url(r'login/$', views.login),
    url(r'register_handle',views.register_handle),
    url(r'index/$',views.index),
]
