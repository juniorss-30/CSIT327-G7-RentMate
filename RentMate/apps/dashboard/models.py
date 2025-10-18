from django.db import models
from django.contrib.auth.models import User

from ..landlord_login.models import LandlordProfile


# Create your models here.
class Tenant(models.Model):
    # tenant account information
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    assigned_landlord = models.ForeignKey(LandlordProfile, on_delete=models.CASCADE, related_name='tenants') #para sa tenant list view
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)

    # tenant rent information
    unit = models.CharField(max_length=50)
    lease_start = models.DateField()
    lease_end = models.DateField()
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default="Paid")
    contract_url = models.URLField()
    status = models.CharField(max_length=20, default="Active")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class MaintenanceRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    date_requested = models.DateField()
    maintenance_type = models.CharField(max_length=20)
    request_status = models.CharField(max_length=20, default="Pending")
    other_description= models.TextField(default="")
    description = models.TextField()

    def __str__(self):
        return f"{self.maintenance_type} - {self.date_requested}"