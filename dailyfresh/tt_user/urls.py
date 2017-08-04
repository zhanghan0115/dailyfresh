from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'register/$', views.register),
    url(r'login/$', views.login),
    url(r'register_handle/$', views.register_handle),
    url(r'login_handle/$', views.login_handle),
    url(r'register_valid/$', views.register_valid),
    url(r'user_center/$',views.user_center),
    url(r'user_order/$', views.user_order),
    url(r'user_site/$', views.user_site),
    url(r'user_loginout',views.user_loginout),
]
