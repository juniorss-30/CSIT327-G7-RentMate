from django import forms
from .models import Tenant, MaintenanceRequest
from django.contrib.auth.models import User
import re

class TenantRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'lease_start': forms.DateInput(attrs={'type': 'date'}),
            'lease_end': forms.DateInput(attrs={'type': 'date'}),
        }
    email = forms.EmailField(max_length=100, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    address = forms.CharField(max_length=100, required=True, widget=forms.TextInput())
    phone_number = forms.CharField(max_length=100, required=True,widget=forms.TextInput())

    unit = forms.CharField(max_length=50, required=True,widget=forms.TextInput())
    lease_start = forms.DateField(required=True,widget=forms.DateInput(attrs={'type': 'date'}   ))
    lease_end = forms.DateField(required=True,widget=forms.DateInput(attrs={'type': 'date'}))
    rent = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    deposit = forms.DecimalField(max_digits=10, decimal_places=2, required=True)

    PAYMENT_STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Overdue', 'Overdue'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Terminated', 'Terminated'),
        ('Pending', 'Pending'),
        ('Expired', 'Expired'),
    ]

    payment_status = forms.ChoiceField(required=True, choices=PAYMENT_STATUS_CHOICES)
    contract_url = forms.URLField(required=True,widget=forms.TextInput())
    status = forms.ChoiceField(required=True, choices=STATUS_CHOICES)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if not self.instance:
            self.fields['password'].initial = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Tenant.objects.filter(user__email=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
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

    def clean(self):
        cleaned_data = super().clean()
        lease_start = cleaned_data.get('lease_start')
        lease_end = cleaned_data.get('lease_end')
        if lease_start and lease_end and lease_end < lease_start:
            raise forms.ValidationError("Lease end date cannot be before start date.")
        return cleaned_data

class MaintenanceRequestForm(forms.ModelForm):
    MAINTENANCE_CHOICES = [
        ('Plumbing', 'Plumbing'),
        ('Electrical', 'Electrical'),
        ('Appliance', 'Appliance'),
        ('Structural', 'Structural'),
        ('Others', 'Others'),
    ]
    maintenance_type = forms.ChoiceField(required=True, choices=MAINTENANCE_CHOICES, label="Choose a Maintenance Option", widget=forms.Select(attrs={'class': 'form-group'}))

    other_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'If others, please provide a description','rows': 2}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Enter description of the Issue','rows': 4}))

    class Meta:
        model = MaintenanceRequest
        fields = ['maintenance_type','other_description','description']