import json
from channels.generic.websocket import AsyncWebsocketConsumer
import datetime


class ChatConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
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
        now = datetime.datetime.now()
        now = now.strftime('%H:%M')
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'time': now,
                'text': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['text']
        now = event['time']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
               'text': message,
               'time': now,

        }))


class AdminChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_group_name = 'admin_room'
        self.user = self.scope['user']
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room = text_data_json['room']
        now = datetime.datetime.now()
        now = now.strftime('%H:%M')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room_catcher',
                'text': message,
                'time': now,
                'room': room

            }
        )

    async def room_catcher(self, event):
        message = event['text']
        now = event['time']
        room = event['room']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
                'text': message,
                'time': now,
                'room': room
        }))