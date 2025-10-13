from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Tenant
from ..landlord_login.models import Landlord
import logging
import re

def home_view(request):
    return render(request, "home_app/home.html")

def tenant_list_view(request):
    return render(request, "home_app/tenant-list.html")

def tenant_register(request):
    if request.method == 'POST':
        #tenant account information
        assigned_landlord = None #TEMPORARY NULL VARIABLE
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password') + '123456' #default password: (last name)123456

        # tenant rent information
        unit = request.POST.get('unit')
        lease_start = request.POST.get('lease_start')
        lease_end = request.POST.get('lease_end')
        rent = request.POST.get('rent')
        deposit = request.POST.get('deposit')
        payment_status = request.POST.get('payment_status')
        contract_url = request.POST.get('contract_url')
        status = request.POST.get('status')

        #Checks if email is already registered in either landlord table or tenant table
        if Tenant.objects.filter(email=email).exists() or Landlord.objects.filter(email=email).exists():
            messages.error(request, 'Email is already used.')
            return render(request,'home_app/tenant-account-register.html',{'data': request.POST})

        #Checks if first name and last name contains numbers
        if not (re.search(r'\d', first_name) or re.search(r'[A-Za-z]', last_name)):
            messages.error(request, 'Name cannot contain numbers or special characters')
            return render(request, 'home_app/tenant-account-register.html', {'data': request.POST})

        #Check if first name and last name contains special characters
        if not (re.search(r'[^A-Za-z0-9]', first_name) or re.search(r'[A-Z]', last_name)):
            messages.error(request, 'Name cannot contain numbers or special characters')
            return render(request, 'home_app/tenant-account-register.html', {'data': request.POST})

        #Checks if phone number contains letters
        if not re.search(r'[a-zA-Z]', phone_number):
            messages.error(request, 'Phone number must not contain characters after “+”')
            return render(request, 'home_app/tenant-account-register.html', {'data': request.POST})

        # Checks if lease number contains letters
        if not (re.search(r'[a-zA-Z]', lease_start) or re.search(r'[a-zA-Z]', lease_end)):
            messages.error(request, 'Lease start/Lease end invalid format')
            return render(request, 'home_app/tenant-account-register.html', {'data': request.POST})

        # Checks if rent contains letters
        if not re.search(r'[a-zA-Z]', rent):
            messages.error(request, 'Rent must not contain letters')
            return render(request, 'home_app/tenant-account-register.html', {'data': request.POST})

        # Checks if deposit contains letters
        if not re.search(r'[a-zA-Z]', deposit):
            messages.error(request, 'Deposit must not contain letters')
            return render(request, 'home_app/tenant-account-register.html', {'data': request.POST})

        #not finished, not sure if assigned Landlord is needed
        #and need to figure out how to assign if it is needed
        tenant = Tenant(
            email=email,
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone_number=phone_number,
            password=password,
            unit=unit,
            lease_start=lease_start,
            lease_end=lease_end,
            rent=rent,
            deposit=deposit,
            payment_status=payment_status,
            contract_url=contract_url,
            status=status,
        )
        #tenant.save()

    return render(request, 'home_app/tenant-account-register.html', {'data': request.POST})
