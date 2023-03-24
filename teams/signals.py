from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Team
from django.core.cache import cache


@receiver(post_save, sender=Team)
def clear_team_cache(sender, instance, created, **kwargs):
    cache_key = f'team_queryset_{instance.id}'
    cache.delete(cache_key)


