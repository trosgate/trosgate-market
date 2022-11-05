import os
from .models import LayoutSetting, GatewaySetting
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


@receiver(post_save, sender=GatewaySetting)
def enforce_default_setting(sender, instance, created, **kwargs):
    '''
    This function ensures that, Balance remains the default,
    We can use sender.objects or modelname.objects
    for readability, modelname is preferred
    '''
    GatewaySetting.objects.filter(default=True).update(default=False)
    GatewaySetting.objects.filter(name='Balance').update(default=True)


#This will clean old banner imae when a new one is uploaded to replace
@receiver(pre_save, sender=LayoutSetting)
def replace_old_banner_with_new_one(sender, instance, **kwargs):
    if instance._state.adding and not instance.pk and not instance.banner_image:
        return False

    try:
        prev_banner = sender.objects.get(pk=instance.pk).banner_image
    except sender.DoesNotExist:
        return False
    
    if prev_banner:
        thumbnail = instance.banner_image
        if not prev_banner == thumbnail:
            if os.path.isfile(prev_banner.path):
                os.remove(prev_banner.path)

