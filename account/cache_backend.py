# from django.core.cache.backends.base import BaseCache
# from django.core.cache import caches

# # cachebackend.py
# class CacheBackend(BaseCache):
#     CACHE_BACKEND_NAME = 'custom_cache'
#     DEFAULT_TIMEOUT = 3600
    
#     @classmethod
#     def get_backend(cls):
#         return caches[cls.CACHE_BACKEND_NAME]
    
#     @classmethod
#     def get(cls, key, default=None, version=None):
#         return cls.get_backend().get(key, default=default, version=version)
    
#     @classmethod
#     def set(cls, key, value, timeout=None, version=None):
#         if timeout is None:
#             timeout = cls.DEFAULT_TIMEOUT
#         cls.get_backend().set(key, value, timeout=timeout, version=version)
    
#     @classmethod
#     def delete(cls, key, version=None):
#         cls.get_backend().delete(key, version=version)
    
#     @classmethod
#     def get_single_object(cls, model, pk, timeout=None, version=None):
#         key = f'{model.__name__}:{pk}'
#         obj = cls.get_backend().get(key, version=version)
#         if obj is None:
#             obj = model.objects.get(pk=pk)
#             cls.get_backend().set(key, obj, timeout=timeout or cls.DEFAULT_TIMEOUT, version=version)
#         else:
#             # add the following code to invalidate cache on object update
#             cached_obj = model.objects.filter(pk=pk).first()
#             if cached_obj is None:
#                 cls.delete(key, version=version)
#             elif cached_obj != obj:
#                 cls.set(key, cached_obj, timeout=timeout or cls.DEFAULT_TIMEOUT, version=version)
#                 obj = cached_obj
#         return obj


#     @classmethod
#     def get_queryset(cls, model, timeout=None, version=None, **filters):
#         key = f'{model.__name__}:{str(filters)}'
#         qs = cls.get_backend().get(key, version=version)
#         if qs is None:
#             qs = model.objects.filter(**filters)
#             cls.get_backend().set(key, qs, timeout=timeout or cls.DEFAULT_TIMEOUT, version=version)
#         else:
#             # check if any object in the queryset has been updated
#             for obj in qs:
#                 obj_key = f'{model.__name__}:{obj.pk}'
#                 cached_obj = cls.get_backend().get(obj_key, version=version)
#                 if cached_obj is None or cached_obj != obj:
#                     # invalidate cache and retrieve updated queryset from database
#                     cls.get_backend().delete(key, version=version)
#                     qs = model.objects.filter(**filters)
#                     cls.get_backend().set(key, qs, timeout=timeout or cls.DEFAULT_TIMEOUT, version=version)
#                     break
#         return qs

#     @classmethod
#     def expire_cache(cls, model=None, pk=None, filters=None, version=None):
#         if model and pk:
#             key = f'{model.__name__}:{pk}'
#             cls.get_backend().delete(key, version=version)
#         elif model and filters:
#             key = f'{model.__name__}:{str(filters)}'
#             cls.get_backend().delete(key, version=version)




# # utilities.py
# def get_single_object(model, pk, timeout=None, version=None, **filters):
#     cache = CustomCache
#     key = f'{model.__name__}:{pk}'
#     obj = cache.get(key, version=version)
#     if obj is None:
#         obj = model.objects.filter(pk=pk, **filters).first()
#         if obj:
#             cache.set(key, obj, timeout=timeout or CustomCache.DEFAULT_TIMEOUT, version=version)
#     return obj

# def get_queryset(model, timeout=None, version=None, **filters):
#     cache = CustomCache
#     key = f'{model.__name__}:{str(filters)}'
#     qs = cache.get(key, version=version)
#     if qs is None:
#         qs = model.objects.filter(**filters)
#         if qs:
#             cache.set(key, qs, timeout=timeout or CustomCache.DEFAULT_TIMEOUT, version=version)
#     else:
#         # check if any object in the queryset has been updated
#         for obj in qs:
#             obj_key = f'{model.__name__}:{obj.pk}'
#             cached_obj = cache.get(obj_key, version=version)
#             if cached_obj is None or cached_obj != obj:
#                 # invalidate cache and retrieve updated queryset from database
#                 cache.delete(key, version=version)
#                 qs = model.objects.filter(**filters)
#                 if qs:
#                     cache.set(key, qs, timeout=timeout or CustomCache.DEFAULT_TIMEOUT, version=version)
#                 break
#     return qs


# # views.py
# from django.shortcuts import get_object_or_404
# from .models import Project, Proposal
# from .utilities import get_single_object, get_queryset

# def project_view(request):
#     merchant = request.GET.get('merchant')
#     team = request.GET.get('team')

#     # get single project based on merchant and team
#     project = get_single_object(Project, merchant=merchant, team=team)
#     if project is None:
#         return HttpResponseNotFound()

#     # get proposals related to project
#     proposals = get_queryset(Proposal, project=project, status=True)

#     # render template with project and proposals
#     return render(request, 'project.html', {'project': project, 'proposals': proposals})


# signals.py
# @receiver(post_save, sender=Project)
# def update_project_cache(sender, instance, **kwargs):
#     cache = caches['custom_cache']
#     key = f'{instance.__class__.__name__}:{instance.pk}'
#     cache.set(key, instance)

# @receiver(post_delete, sender=Project)
# def expire_project_cache(sender, instance, **kwargs):
#     cache = caches['custom_cache']
#     key = f'{instance.__class__.__name__}:{instance.pk}'
#     cache.delete(key)

# @receiver(post_save, sender=Proposal)
# def update_proposal_cache(sender, instance, **kwargs):
#     cache = caches['custom_cache']
#     key = f'{instance.__class__.__name__}:{instance.pk}'
#     cache.set(key, instance)

# @receiver(post_delete, sender=Proposal)
# def expire_proposal_cache(sender, instance, **kwargs):
#     cache = caches['custom_cache']
#     key = f'{instance.__class__.__name__}:{instance.pk}'
#     cache.delete(key)
