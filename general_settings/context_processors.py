from .models import Category, WebsiteSetting, AutoLogoutSystem
from django.contrib.sites.models import Site


def categories(request):
    if Category.objects.count():
        categories = Category.objects.filter(visible=True)
        return {'categories': categories}
    return {'categories':None}


def website(request):
    site = Site.objects.get_current()
    merchant = request.merchant
    parent = request.parent_site
    if merchant is not None and site == merchant:
        return {'website': request.site.merchant}
    if parent is not None and site == parent:
        return {'website': request.site.websitesetting}


def autoLogoutSystem(request):
    if AutoLogoutSystem.objects.filter(pk=1).exists():
        autoLogoutSystem = AutoLogoutSystem.objects.get(pk=1)
        return {'autoLogoutSystem': autoLogoutSystem}
    return {'autoLogoutSystem':None}    

   