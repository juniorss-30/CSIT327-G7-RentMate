from django.contrib import admin
from .models import Tenant, MaintenanceRequest

# Register your models here.
admin.site.register(Tenant)
admin.site.register(MaintenanceRequest)