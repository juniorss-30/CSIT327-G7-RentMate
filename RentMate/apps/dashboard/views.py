from django.shortcuts import render


def home_view(request):
    return render(request, "home_app/home.html")

def tenant_list_view(request):
    return render(request, "home_app/tenant-list.html")

def tenant_account_register_view(request):
    return render(request, "home_app/tenant-account-register.html")
