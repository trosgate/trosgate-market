from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from . models import Currency, WebsiteSetting
from django.contrib.sites.models import Site
from django.core.cache import cache



@receiver(post_save, sender=Site)
def invalidate_allowed_domains_cache(sender, instance, **kwargs):
    # Invalidate the cached list of allowed domains
    print('Invalidate the cached list of allowed domains')
    cache.delete('allowed_domains_cache')


@receiver(post_save, sender=Currency)
def create_or_only_one_default_currency(sender, instance, created, **kwargs):
    if instance.id and instance.default == True:
        Currency.objects.filter(default=True).update(default=False)
        Currency.objects.filter(id=instance.id).update(supported=True, default=True)

    if Currency.objects.count() and Currency.objects.filter(default=True).count() == 0:
        currency = Currency.objects.last()
        currency.supported=True
        currency.default=True
        currency.save()


# #This will clean old banner imae when a new one is uploaded to replace
@receiver(pre_save, sender=WebsiteSetting)
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














