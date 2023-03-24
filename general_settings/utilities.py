from . models import WebsiteSetting
from django.contrib.sites.models import Site

def website_name():
    try:
        return Site.objects.get_current().name
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
        website_setting = Site.objects.get_current()
        return f'{get_protocol_only()}{website_setting.domain}'
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
    

 




