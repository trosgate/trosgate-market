from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from django.utils.timesince import timesince
from .models import Room, Message
from account.models import Customer, Merchant
from django.contrib.sites.models import Site



class NotifierConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        header = dict(self.scope['headers'])
        domain = header[b'host'].decode('utf-8').lower().split(':')[0]
        if domain.startswith('www.'):
            domain = domain[4:]
        self.host = domain

        await self.get_room()
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        type = text_data_json['type']
        guest = text_data_json['guest']
        agent = text_data_json.get('agent', '')

        if type == 'message':
            new_message = await self.create_message(guest, message, agent)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'guest': guest,
                    'agent': agent,
                    'created_at': timesince(new_message.created_at),
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'guest': event['guest'],
            'agent': event['agent'],
            'created_at': event['created_at'],
        }))
    
    @sync_to_async
    def get_room(self):
        merchant = Merchant.objects.filter(site__domain=self.host).first()
        self.room = Room.objects.filter(reference=self.room_name, merchant=merchant).last()


    @sync_to_async
    def create_message(self, sender, message, agent):
        merchant = Merchant.objects.filter(site__domain=self.host).first()
        new_message = Message.objects.create(content=message, sender=sender, merchant=merchant)
        if agent:
            new_message.created_by = Customer.objects.filter(pk=agent).first()
            new_message.save()
        
        self.room.messages.add(new_message)

        return new_message