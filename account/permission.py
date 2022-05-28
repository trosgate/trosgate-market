from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from . models import Customer

def user_is_freelancer(function):

    def wrap(request, *args, **kwargs):   

        if request.user.user_type == Customer.FREELANCER:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_client(function):

    def wrap(request, *args, **kwargs):    

        if request.user.user_type == Customer.CLIENT:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap