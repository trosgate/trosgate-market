from django.shortcuts import redirect
from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404
from django.urls import reverse


class AdminGateMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):

        if request.path.startswith('/admin'):
            if request.user.is_authenticated:
                if not request.user.is_staff:
                    raise Http404

        return self.get_response(request)


























