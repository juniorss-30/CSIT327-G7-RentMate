from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('tenant_list/', views.tenant_list_view, name='tenant_list'),
    path('tenant/register/', views.tenant_register, name='tenant_register'),
    path('tenant/edit/<int:tenant_id>/', views.edit_tenant, name='edit_tenant'),
    path('tenant/delete/<int:tenant_id>/', views.delete_tenant, name='delete_tenant'),
    path('tenant_list/', views.tenant_list_view, name='tenant_list'),
    path('tenant/login/', views.tenant_login, name='tenant_login'),
    path('tenant/change-password/', views.tenant_change_password, name='tenant_change_password'),
]
