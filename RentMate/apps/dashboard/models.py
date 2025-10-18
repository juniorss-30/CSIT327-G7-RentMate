from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Tenant(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    unit = models.CharField(max_length=50)
    lease_start = models.DateField()
    lease_end = models.DateField()
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default="Pending")
    contract_url = models.URLField()
    status = models.CharField(max_length=20, default="Active")

    first_login = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class MaintenanceRequest(models.Model):
    requester = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    date_requested = models.DateField()
    maintenance_type = models.CharField(max_length=20)
    request_status = models.CharField(max_length=20, default="Pending")
    other_description = models.TextField(blank=True, default="")
    description = models.TextField()

    def __str__(self):
        return f"{self.maintenance_type} - {self.date_requested}"
