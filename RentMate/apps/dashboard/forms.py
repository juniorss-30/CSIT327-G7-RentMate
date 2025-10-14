from django import forms
from .models import Tenant
import re

class TenantRegisterForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    address = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=15, required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    unit = forms.CharField(max_length=50)
    lease_start = forms.DateField()
    lease_end = forms.DateField()
    rent = forms.FloatField()
    deposit = forms.FloatField()
    payment_status = forms.CharField(max_length=50)
    contract_url = forms.URLField(required=False)
    status = forms.CharField(max_length=50)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Tenant.objects.filter(email=email).exists() or Landlord.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already used.')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if re.search(r'[^A-Za-z]', first_name):
            raise forms.ValidationError('First name cannot contain numbers or special characters.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if re.search(r'[^A-Za-z]', last_name):
            raise forms.ValidationError('Last name cannot contain numbers or special characters.')
        return last_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if re.search(r'[a-zA-Z]', phone_number):
            raise forms.ValidationError('Phone number must not contain letters.')
        return phone_number

    def clean_lease_start(self):
        lease_start = self.cleaned_data.get('lease_start')
        if lease_start is None:
            raise forms.ValidationError('Lease start date is required.')
        return lease_start

    def clean_lease_end(self):
        lease_end = self.cleaned_data.get('lease_end')
        if lease_end is None:
            raise forms.ValidationError('Lease end date is required.')
        return lease_end

    def clean_rent(self):
        rent = self.cleaned_data.get('rent')
        if rent is None or not isinstance(rent, (int, float)):
            raise forms.ValidationError('Rent must be a number.')
        return rent

    def clean_deposit(self):
        deposit = self.cleaned_data.get('deposit')
        if deposit is None or not isinstance(deposit, (int, float)):
            raise forms.ValidationError('Deposit must be a number.')
        return deposit

    def clean(self):
        cleaned_data = super().clean()
        lease_start = cleaned_data.get('lease_start')
        lease_end = cleaned_data.get('lease_end')
        if lease_start and lease_end and lease_end < lease_start:
            raise forms.ValidationError("Lease end date cannot be before start date.")
