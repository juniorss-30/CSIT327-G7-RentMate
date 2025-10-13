from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Landlord
from ..dashboard.models import Tenant
import logging
import re

# Initialize logger
logger = logging.getLogger(__name__)

def landlord_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        #checks if email is registered in Landlord table in database
        try:
            landlord = Landlord.objects.get(email=email)
        except Landlord.DoesNotExist:
            messages.error(request, 'Invalid Credentials')
            logger.warning(f"Login attempt with non-existing email: {email}")
            return render(request, 'logins/landlord-login.html')

        if landlord.password == password:
            return redirect('home') # Redirect to dashboard
        messages.error(request, 'Invalid Credentials')
        logger.warning(f"Failed landlord login attempt with email: {email}")

    return render(request, 'logins/landlord-login.html')

def tenant_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # checks if email is registered in Tenant table in database
        try:
            tenant = Tenant.objects.get(email=email)
        except:
            messages.error(request, 'Invalid Credentials')
            logger.warning(f"Login attempt with non-existing email: {email}")
            return render(request, 'logins/tenant-login.html')
    return render(request, 'logins/tenant-login.html')

def index(request):
    return render(request, 'index.html')  # Render the main landing page

def landlord_register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        #Checks if phone number contains letters
        if re.search(r'[A-Za-z]', phone_number):
            messages.error(request, 'Phone number must not contain letters.')
            return render(request, 'logins/landlord-register.html', {'data': request.POST})

        #Checks if phone number is valid Philippine number
        if not (phone_number.startswith('+63') or phone_number.startswith('09')):
            messages.error(request, 'Phone number must start with +63 or 09')
            return render(request, 'logins/landlord-register.html', {'data': request.POST})

        if phone_number.startswith('+63'):
            if len(phone_number) != 12:
                messages.error(request, 'Phone number must have 11 digits.')
                return render(request, 'logins/landlord-register.html', {'data': request.POST})
        if phone_number.startswith('09'):
            if len(phone_number) != 11:
                messages.error(request, 'Phone number must have 11 digits.')
                return render(request, 'logins/landlord-register.html', {'data': request.POST})

        #Checks if password is in valid format
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters and include letters, numbers, and a special character.')
            return render(request, 'logins/landlord-register.html', {'data': request.POST})

        #Checks if password contains letters
        if not re.search(r'[A-Za-z]', password):
            messages.error(request, 'Password must be at least 8 characters and include letters, numbers, and a special character.')
            return render(request, 'logins/landlord-register.html', {'data': request.POST})

        #Checks if password contains numbers
        if not re.search(r'\d', password):
            messages.error(request, 'Password must be at least 8 characters and include letters, numbers, and a special character.')
            return render(request, 'logins/landlord-register.html', {'data': request.POST})

        #Check if password contains special characters
        if not re.search(r'[^A-Za-z0-9]', password):
            messages.error(request, 'Password must be at least 8 characters and include letters, numbers, and a special character.')
            return render(request, 'logins/landlord-register.html', {'data': request.POST})
        
        # Validate passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'logins/landlord-register.html', {'data': request.POST})

        # Checks if email exits
        if Landlord.objects.filter(email=email).exists():
            messages.error(request, 'Email is already used.')
            return render(request, 'logins/landlord-register.html', {'data': request.POST})

        landlord = Landlord(
            email=email,
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone_number=phone_number,
            password=password,
        )
        landlord.save()

        # Here you would typically create a new user in the database
        # For now, we'll just show a success message
        messages.success(request, 'Registration successful! Please login.')
        logger.info(f"New landlord registered: {first_name} {last_name}")
        return redirect('landlord_login')
    
    return render(request, 'logins/landlord-register.html', {'data': request.POST})



