from .models import Category, WebsiteSetting, AutoLogoutSystem


def categories(request):
    return {
        'categories': Category.objects.filter(visible=True)
    }


def website(request):
    if WebsiteSetting.objects.filter(pk=1).exists():
        website = WebsiteSetting.objects.get(pk=1)
        return {'website': website}
        
    else:
        website = WebsiteSetting.objects.create(
            pk=1, site_name='Trosgate',
            tagline='Freelance marketplace saas',
            site_description='Freelance marketplace saas',
            protocol='https://',
            site_domain='trosgate.com',
            twitter_url='https://trosgate.com',
            instagram_url='https://trosgate.com',
            youtube_url='https://trosgate.com',
            facebook_url='https://trosgate.com'
        )
        return {'website': website}


def autoLogoutSystem(request):
    if WebsiteSetting.objects.filter(pk=1).exists():
        autoLogoutSystem = AutoLogoutSystem.objects.get(pk=1)
        return {'autoLogoutSystem': autoLogoutSystem}
    else:
         return {'autoLogoutSystem':None}    

   