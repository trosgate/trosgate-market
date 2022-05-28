from .models import WebsiteSetting, AutoLogoutSystem


def website(request):
    try:
        return {'website': WebsiteSetting.objects.get(id=1)}
    except:
         return {'website':None}


def autoLogoutSystem(request):
    try:
        return {'autoLogoutSystem': AutoLogoutSystem.objects.get(id=1)}
    except:
         return {'autoLogoutSystem':None}    

   