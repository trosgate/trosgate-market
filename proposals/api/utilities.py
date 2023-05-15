from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


def get_object_or_404_response(klass, *arg, **kwargs):
    try:
        return klass.objects.get(*arg, **kwargs)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # return obj if isinstance(obj, Model) else Response(status=status.HTTP_404_NOT_FOUND)
    