from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from django.utils.timesince import timesince
from .models import Room, Message
from account.models import Customer, Merchant
from django.contrib.sites.models import Site
from urllib.parse import parse_qs


class NotifierConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']
        query_param = dict(parse_qs(self.scope['query_string'].decode('utf-8')))
        self.host = query_param['site'][0]

        await self.get_room()
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # notify user
        # if self.user.us_authenticated:


    async def disconnect(self, close_code):
        # Leave room group
        if not self.user.is_authenticated:
            await self.close_chat()
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
        agentid = text_data_json.get('agentid', '')

        if type == 'message':
            new_message = await self.create_message(guest, message, agentid)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'guest': guest,
                    'agent': agent,
                    'agentid': agentid,
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
            'agentid': event['agentid'],
            'created_at': event['created_at'],
        }))
    
    @sync_to_async
    def get_room(self):
        merchant = Merchant.objects.filter(pk=self.host).first()
        self.room = Room.objects.filter(reference=self.room_name, merchant=merchant).last()
    

    @sync_to_async
    def close_chat(self):
        merchant = Merchant.objects.filter(pk=self.host).first()
        self.room = Room.objects.filter(reference=self.room_name, merchant=merchant).last()
        self.room.status = Room.CLOSED
        self.room.save()


    @sync_to_async
    def create_message(self, sender, message, agentid):
        merchant = Merchant.objects.filter(pk=self.host).first()
        new_message = Message.objects.create(content=message, sender=sender, merchant=merchant)
        if agentid:
            user = Customer.objects.filter(pk=agentid).first()
            new_message.created_by = user
            new_message.sender = user.get_short_name()
            new_message.save()
        
        self.room.messages.add(new_message)

        return new_message
    