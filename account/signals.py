from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from . models import Customer, TwoFactorAuth, Merchant
from django.core.cache import cache
from django.core.cache import caches
from teams.models import Package


@receiver(post_save, sender=Customer)
def generate_TwoFactorAuth_code(sender, instance, created, **kwargs):
    if created:
        TwoFactorAuth.objects.create(user=instance)

# @receiver(post_save, sender=Merchant)
# def create_upsell_plans(sender, instance, created, **kwargs):
#     if created:
#         plans = ['basic', 'team']
#         TwoFactorAuth.objects.create(user=instance)
        

@receiver(post_save, sender=Merchant)
def clear_team_cache(sender, instance, created, **kwargs):
    cache_key = f'merchant_queryset_{instance.merchant.active_merchant_id}'
    print('initial cache_key', cache_key)
    cache.delete(cache_key)
    print('later cache_key', cache_key)


