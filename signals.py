
# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import caches
from .models import Project, Proposal


@receiver(post_save, sender=Project)
def update_project_cache(sender, instance, **kwargs):
    cache = caches['custom_cache']
    key = f'{instance.__class__.__name__}:{instance.pk}'
    cache.set(key, instance)

@receiver(post_delete, sender=Project)
def expire_project_cache(sender, instance, **kwargs):
    cache = caches['custom_cache']
    key = f'{instance.__class__.__name__}:{instance.pk}'
    cache.delete(key)

@receiver(post_save, sender=Proposal)
def update_proposal_cache(sender, instance, **kwargs):
    cache = caches['custom_cache']
    key = f'{instance.__class__.__name__}:{instance.pk}'
    cache.set(key, instance)

@receiver(post_delete, sender=Proposal)
def expire_proposal_cache(sender, instance, **kwargs):
    cache = caches['custom_cache']
    key = f'{instance.__class__.__name__}:{instance.pk}'
    cache.delete(key)
