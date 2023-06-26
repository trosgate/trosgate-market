import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from account.models import Customer, Merchant
from django.contrib.sessions.models import Session
from .models import Room
from django.views.decorators.http import require_POST
from teams.utilities import create_random_code



@require_POST
def create_room(request, room_name):
    data = json.loads(request.body)

    page_name = data.get('url', '')
    guest = data.get('guestname', '')
    
    Room.objects.create(reference=room_name, guest=guest, page_name=page_name)
    return JsonResponse({'room':'success'})


@login_required
def chatroom(request):
    agents=request.merchant.members.all()
    for agent in agents:
        print(agent.email)
    rooms = Room.objects.filter(merchant=request.merchant, merchant__members__in=[request.user])
    return render(request, 'notification/chatroom.html', {'rooms':rooms, 'agents':agents})


@login_required
def support_chatroom(request, room_name):
    room = get_object_or_404(Room, reference=room_name, merchant__id=request.user.active_merchant_id)

    if room.status == Room.WAITING:
        room.status = Room.ACTIVE
        room.agent = request.user
        room.save()
    
    rooms = room.messages.all().order_by('created_at')
    context = {
        'room':room,
        'rooms':rooms,

    }   
    return render(request, 'notification/join_chatroom.html', context)


@login_required
@require_POST
def remove_chatroom(request):
    room_id = request.POST.get('room_id')
    room = get_object_or_404(Room, pk=room_id, merchant=request.merchant)
    room.messages.all().delete()
    room.delete()
    rooms = Room.objects.filter(merchant=request.merchant)
    return render(request, 'notification/partials/chatroom.html', {'rooms':rooms})

