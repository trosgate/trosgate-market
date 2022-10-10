import os
from .models import LayoutSetting
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

@receiver(pre_save, sender=LayoutSetting)
def replace_old_banner_with_new_one(sender, instance, **kwargs):
    if instance._state.adding and not instance.pk:
        return False
    
    try:
        prev_banner = sender.objects.get(pk=instance.pk).banner_image
    except sender.DoesNotExist:
        return False
    
    thumbnail = instance.banner_image
    if not prev_banner == thumbnail:
        if os.path.isfile(prev_banner.path):
            os.remove(prev_banner.path)

