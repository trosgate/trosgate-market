# utilities.py
def get_single_object(model, pk, timeout=None, version=None, **filters):
    cache = CustomCache
    key = f'{model.__name__}:{pk}'
    obj = cache.get(key, version=version)
    if obj is None:
        obj = model.objects.filter(pk=pk, **filters).first()
        if obj:
            cache.set(key, obj, timeout=timeout or CustomCache.DEFAULT_TIMEOUT, version=version)
    return obj

def get_queryset(model, timeout=None, version=None, **filters):
    cache = CustomCache
    key = f'{model.__name__}:{str(filters)}'
    qs = cache.get(key, version=version)
    if qs is None:
        qs = model.objects.filter(**filters)
        if qs:
            cache.set(key, qs, timeout=timeout or CustomCache.DEFAULT_TIMEOUT, version=version)
    else:
        # check if any object in the queryset has been updated
        for obj in qs:
            obj_key = f'{model.__name__}:{obj.pk}'
            cached_obj = cache.get(obj_key, version=version)
            if cached_obj is None or cached_obj != obj:
                # invalidate cache and retrieve updated queryset from database
                cache.delete(key, version=version)
                qs = model.objects.filter(**filters)
                if qs:
                    cache.set(key, qs, timeout=timeout or CustomCache.DEFAULT_TIMEOUT, version=version)
                break
    return qs


# views.py
from django.shortcuts import get_object_or_404
from .models import Project, Proposal
from .utilities import get_single_object, get_queryset

def project_view(request):
    merchant = request.GET.get('merchant')
    team = request.GET.get('team')

    # get single project based on merchant and team
    project = get_single_object(Project, merchant=merchant, team=team)
    if project is None:
        return HttpResponseNotFound()

    # get proposals related to project
    proposals = get_queryset(Proposal, project=project, status=True)

    # render template with project and proposals
    return render(request, 'project.html', {'project': project, 'proposals': proposals})

