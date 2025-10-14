from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('tenant_list/', views.tenant_list_view, name='tenant_list'),
    path('tenant/register/', views.tenant_register, name='tenant_register'),
]
