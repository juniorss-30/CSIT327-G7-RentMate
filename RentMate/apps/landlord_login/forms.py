from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
import re

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class LandlordRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100,required=True,widget=forms.PasswordInput(attrs={'id': 'confirm_password'}))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(attrs={'id': 'email','required': True}),
            'first_name': forms.TextInput(attrs={'id': 'first_name','required': True}),
            'last_name': forms.TextInput(attrs={'id': 'last_name','required': True}),
        }
    address = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'id': 'address',}))
    phone_number = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'id': 'phone_number',}))
    password = forms.CharField(max_length=128,required=True,widget=forms.PasswordInput(attrs={'id': 'password',}))

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        # Check if phone number contains letters
        if re.search(r'[A-Za-z]', phone_number):
            raise ValidationError('Phone number must not contain letters.')

        # Check if phone number is valid Philippine number
        if not (phone_number.startswith('+63') or phone_number.startswith('09')):
            raise ValidationError('Phone number must start with +63 or 09')

        # Check phone number length
        if phone_number.startswith('+63') and len(phone_number) != 13:
            raise ValidationError('Phone number must have 10 digits after +63.')
        if phone_number.startswith('09') and len(phone_number) != 11:
            raise ValidationError('Phone number must have 9 digits after 09.')
        return phone_number

    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = ""
        if len(password) < 8:
            errors += ' be at least 8 characters,'
        if not re.search(r'[A-Za-z]', password):
            errors += ' include letters,'
        if not re.search(r'\d', password):
            errors += ' include numbers,'
        if not re.search(r'[^A-Za-z0-9]', password):
            errors += ' include special characters,'
        if errors:
            raise ValidationError("Password must" + errors)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match.')

        # Check if email already exists
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email is already used.')

        return cleaned_data
