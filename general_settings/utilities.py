from . models import WebsiteSetting


def website_name():
    try:
        return WebsiteSetting.objects.get(pk=1).site_name
    except:
        return None

def get_protocol_only():
    try:
        website_setting = WebsiteSetting.objects.get(pk=1)
        return website_setting.protocol
    except:
        website_setting = None
        return 'http://'

def get_protocol_with_domain_path():
    try:
        website_setting = WebsiteSetting.objects.get(pk=1)
        return f'{website_setting.protocol}{website_setting.site_domain}'
    except:
        return None

def get_twitter_path():
    try:
        return WebsiteSetting.objects.get(pk=1).twitter_url
    except:
        return None    
    
def get_youtube_path():
    try:
        return WebsiteSetting.objects.get(pk=1).youtube_url
    except:
        return None     

def get_facebook_path():
    try:
        return WebsiteSetting.objects.get(pk=1).facebook_url
    except:
        return None     
    
def get_instagram_path():
    try:
        return WebsiteSetting.objects.get(pk=1).instagram_url
    except:
        return None     
    

 




