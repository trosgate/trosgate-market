import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from account.models import Customer
from django.contrib.sessions.models import Session
from .models import Room
from django.views.decorators.http import require_POST
from teams.utilities import create_random_code


@require_POST
def create_room(request, reference):
    data = json.loads(request.body)

    page_name = data.get('url', '')
    guest = data.get('guestname', '')
    
    Room.objects.create(reference=reference, guest=guest, page_name=page_name)
    return JsonResponse({'room':'success'})


def chatroom(request, room_name):
    # room = Room.objects.get(reference=room_name)
    # return JsonResponse({'room':room}, safe=False)
    return render(request, 'notification/partials/helpdesk.html', {'room':room_name})
