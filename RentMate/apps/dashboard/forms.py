from django import forms
from .models import Tenant
import re

class TenantRegisterForm(forms.ModelForm):

    class Meta:
        model = Tenant
        fields = [
            'email', 'first_name', 'last_name', 'address',
            'phone_number', 'password', 'unit', 'lease_start',
            'lease_end', 'rent', 'deposit', 'payment_status',
            'contract_url', 'status'
        ]
        widgets = {
            'password': forms.PasswordInput,
        }