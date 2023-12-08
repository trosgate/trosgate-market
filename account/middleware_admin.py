from django.shortcuts import redirect
from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404
from django.urls import reverse
from threadlocals.threadlocals import set_thread_variable


class AdminGateMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        
        if request.path.startswith('/admin'):
            if request.user.is_authenticated:
                set_thread_variable('parent_user', request.user)
                print(request.user.is_staff)
                if not request.user.is_staff:
                    raise Http404

        return self.get_response(request)


























