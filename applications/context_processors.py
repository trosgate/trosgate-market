from .application import ApplicationAddon

def application_addon(request):
    return {'application_addon': ApplicationAddon(request)}


