from django.conf import settings
from account.models import Customer, Merchant
from django.core.cache import cache


def active_merchant(request):
    if request.user.is_authenticated and request.user.user_type == Customer.MERCHANT:
        cache_key = f'merchant_queryset_{request.user.active_merchant_id}'
        active_merchant = cache.get(cache_key)
        if active_merchant:   
            return {'active_merchant':active_merchant}
    
        elif active_merchant is None and request.user.active_merchant_id:
            active_merchant = Merchant.objects.get(pk=request.user.active_merchant_id, members__in=[request.user])
            cache.set(cache_key, active_merchant, settings.CACHE_TTL)
            return {'active_merchant':active_merchant}

    return {'active_merchant':None}

