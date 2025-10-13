from django import forms
from .models import Landlord


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class LandlordRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Landlord
        fields = ['email', 'first_name', 'last_name', 'address', 'phone_number', 'password']
        widgets = {
            'password': forms.PasswordInput,
        }
