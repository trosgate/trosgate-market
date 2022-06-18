from .models import Category, WebsiteSetting, AutoLogoutSystem


def categories(request):
    return {
        'categories': Category.objects.filter(visible=True)
    }


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

   