from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction

from .forms import TenantRegisterForm, MaintenanceRequestForm
from .models import Tenant, MaintenanceRequest
from..landlord_login.models import LandlordProfile
from django.contrib.auth.decorators import login_required

@login_required(login_url='landlord_login')
def home_view(request):
    return render(request, "home_app/home.html")

@login_required(login_url='landlord_login')
def tenant_list_view(request):
    tenants = Tenant.objects.all()
    return render(request, "home_app/tenant-list.html")

@transaction.atomic # Creating a tenant
def tenant_register(request):
    if not request.user.is_authenticated:
        return redirect('landlord_login')
    if request.method == 'POST':
        form = TenantRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['last_name'] + '123456',
            )

            Tenant.objects.create(
                user=user,
                assigned_landlord=LandlordProfile.objects.get(user=request.user),
                address=form.cleaned_data['address'],
                phone_number=form.cleaned_data['phone_number'],
                unit=form.cleaned_data['unit'],
                lease_start=form.cleaned_data['lease_start'],
                lease_end=form.cleaned_data['lease_end'],
                rent=form.cleaned_data['rent'],
                deposit=form.cleaned_data['deposit'],
                payment_status=form.cleaned_data['payment_status'],
                contract_url=form.cleaned_data['contract_url'],
                status=form.cleaned_data['status']
            )
            messages.success(request, 'Tenant created successfully!')
            return redirect('tenant_list')
    else:
        form = TenantRegisterForm()
    return render(request, 'home_app/tenant-account-register.html', {'form': form})


# Editing a tenant
def edit_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)

    if request.method == 'POST':
        form = TenantRegisterForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tenant updated successfully!')
            return redirect('tenant_list')
    else:
        form = TenantRegisterForm(instance=tenant)

    return render(request, 'home_app/tenant-account-register.html', {
        'form': form,
        'edit_mode': True
    })


def delete_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    tenant.delete()
    messages.success(request, 'Tenant deleted successfully!')
    return redirect('tenant_list')


#Tenant Side Dashboard
@login_required(login_url='tenant_login')
def tenant_home_view(request):
    return render(request, "home_app_tenant/tenant-home.html")

@login_required(login_url='tenant_login')
def tenant_maintenance_add_view(request):
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            MaintenanceRequest.objects.create(
                requester=request.user,
                date_requested = timezone.localtime().date(),
                maintenance_type = form.cleaned_data['maintenance_type'],
                other_description = form.cleaned_data['other_description'],
                description = form.cleaned_data['description'],
            )
            messages.success(request, 'Maintenance request created successfully!')
            return render(request,'home_app_tenant/tenant-maintenance.html', {'form': form})
    else:
        form =MaintenanceRequestForm()
    return render(request,'home_app_tenant/tenant-maintenance.html', {'form': form})