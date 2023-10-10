from .models import Category, WebsiteSetting, AutoLogoutSystem
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site



def categories(request):
    if Category.objects.count():
        categories = Category.objects.filter(visible=True)
        return {'categories': categories}
    return {'categories':None}


def website(request):
    current_site = get_current_site(request)
    website_obj = None

    if hasattr(current_site, 'websitesetting') and current_site.websitesetting:
        website_obj = request.parent_site
        
    elif hasattr(current_site, 'merchant') and current_site.merchant:
        website_obj = request.merchant
        
    return {'website': website_obj}


def autoLogoutSystem(request):
    return {'autoLogoutSystem':AutoLogoutSystem.objects.first()}    
    # if AutoLogoutSystem.objects.filter(pk=1).exists():
    #     autoLogoutSystem = AutoLogoutSystem.objects.get(pk=1)
    #     return {'autoLogoutSystem': autoLogoutSystem}
    # return {'autoLogoutSystem':None}    

   