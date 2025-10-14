from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TenantRegisterForm
from .models import Tenant

def tenant_register(request):
    if request.method == 'POST':
        form = TenantRegisterForm(request.POST)
        if form.is_valid():
            tenant = Tenant.objects.create(
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                address=form.cleaned_data['address'],
                phone_number=form.cleaned_data['phone_number'],
                password=form.cleaned_data['last_name'] + '123456',
                unit=form.cleaned_data['unit'],
                lease_start=form.cleaned_data['lease_start'],
                lease_end=form.cleaned_data['lease_end'],
                rent=form.cleaned_data['rent'],
                deposit=form.cleaned_data['deposit'],
                payment_status=form.cleaned_data['payment_status'],
                contract_url=form.cleaned_data['contract_url'],
                status=form.cleaned_data['status']
            )
            messages.success(request, f'Tenant account created for {tenant.first_name} {tenant.last_name}!')
            return redirect('tenant_list')
    else:
        form = TenantRegisterForm()

    return render(request, 'home_app/tenant-account-register.html', {'form': form})


def home_view(request):
    return render(request, "home_app/home.html")


def tenant_list_view(request):
    return render(request, "home_app/tenant-list.html")
