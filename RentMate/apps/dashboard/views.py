from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .forms import TenantRegisterForm, MaintenanceRequestForm
from .models import Tenant, MaintenanceRequest


@login_required(login_url='landlord_login')
def home_view(request):
    return render(request, "home_app/home.html")


@login_required(login_url='landlord_login')
def tenant_list_view(request):
    tenants = Tenant.objects.all()
    return render(request, "home_app/tenant-list.html", {'tenants': tenants})


def tenant_register(request):
    if not request.user.is_authenticated:
        return redirect('landlord_login')

    if request.method == 'POST':
        form = TenantRegisterForm(request.POST)
        if form.is_valid():
            tenant = form.save(commit=False)
            tenant.first_login = True
            tenant.is_active = False
            tenant.status = 'Inactive'
            tenant.save()

            temp_password = form.cleaned_data['password']

            send_mail(
                'Your Tenant Account - RentMate',
                f"""
Hi {tenant.first_name},

Your account has been created.

Email: {tenant.email}
Temporary Password: {temp_password}

Please log in at: http://127.0.0.1:8000/home/tenant/login/

Thank you,
RentMate Team
""",
                settings.EMAIL_HOST_USER,
                [tenant.email],
                fail_silently=False
            )

            messages.success(request, 'Tenant created successfully! Credentials sent via email.')
            return redirect('tenant_list')
    else:
        form = TenantRegisterForm()

    return render(request, 'home_app/tenant-account-register.html', {'form': form})


def edit_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        form = TenantRegisterForm(request.POST, instance=tenant)
        if form.is_valid():
            if 'password' in form.cleaned_data and form.cleaned_data['password']:
                tenant.set_password(form.cleaned_data['password'])
            form.save()
            tenant.save()
            messages.success(request, 'Tenant updated successfully!')
            return redirect('tenant_list')
    else:
        form = TenantRegisterForm(instance=tenant)

    return render(request, 'home_app/tenant-account-register.html', {'form': form, 'edit_mode': True})


def delete_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    tenant.delete()
    messages.success(request, 'Tenant deleted successfully!')
    return redirect('tenant_list')


# --- Tenant Dashboard ---

@login_required(login_url='tenant_login')
def tenant_home_view(request):
    tenant_id = request.session.get("tenant_id")
    if not tenant_id:
        return redirect('tenant_login')
    return render(request, "home_app_tenant/tenant-home.html")


@login_required(login_url='tenant_login')
def tenant_maintenance_add_view(request):
    tenant_id = request.session.get("tenant_id")
    if not tenant_id:
        return redirect('tenant_login')
    tenant = Tenant.objects.get(id=tenant_id)

    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            MaintenanceRequest.objects.create(
                requester=tenant,
                date_requested=timezone.localtime().date(),
                maintenance_type=form.cleaned_data['maintenance_type'],
                other_description=form.cleaned_data['other_description'],
                description=form.cleaned_data['description']
            )
            messages.success(request, 'Maintenance request created successfully!')
            return render(request, 'home_app_tenant/tenant-maintenance.html', {'form': form})
    else:
        form = MaintenanceRequestForm()
    return render(request, 'home_app_tenant/tenant-maintenance.html', {'form': form})


# --- Tenant Authentication ---

def tenant_login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            tenant = Tenant.objects.get(email=email)
        except Tenant.DoesNotExist:
            messages.error(request, "Invalid credentials.")
            return redirect("tenant_login")

        if tenant.check_password(password):
            request.session["tenant_id"] = tenant.id
            if tenant.first_login:
                messages.info(request, "Update password required.")
                return redirect("tenant_change_password")
            else:
                tenant.is_active = True
                tenant.save()
                return redirect("tenant_home")
        else:
            messages.error(request, "Invalid credentials.")
            return redirect("tenant_login")

    return render(request, "logins/tenant-login.html")


def tenant_change_password(request):
    tenant_id = request.session.get("tenant_id")
    if not tenant_id:
        return redirect("tenant_login")

    tenant = Tenant.objects.get(id=tenant_id)

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password == confirm_password:
            tenant.set_password(password)
            tenant.first_login = False
            tenant.is_active = True
            tenant.save()
            messages.success(request, "Password updated successfully! You can now login.")
            return redirect("tenant_login")
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, "home_app/tenant-change-password.html")
